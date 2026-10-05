from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.backend.observability import configure_logging, get_correlation_id, logger, set_correlation_id, Timer
from app.backend.routes import router
from app.backend.services import services
from app.backend.settings import settings

configure_logging(settings.log_level)

app = FastAPI(title="Clinical AI Evaluation Lab", version="0.4.0", description="API for the CAIEL clinical AI evaluation platform.")
app.include_router(router, prefix="/api/v1")

@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    return response

@app.middleware("http")
async def observability_middleware(request: Request, call_next):
    correlation_id = request.headers.get("X-Correlation-ID") or set_correlation_id()
    set_correlation_id(correlation_id)
    timer = Timer.start()
    response = None
    try:
        response = await call_next(request)
        return response
    except Exception:
        logger.exception("request_failed")
        raise
    finally:
        status_code = response.status_code if response is not None else 500
        logger.info("request_completed", extra={"request_id": correlation_id, "latency_ms": timer.elapsed_ms(), "status_code": status_code})
        if response is not None:
            response.headers["X-Correlation-ID"] = get_correlation_id()

@app.get("/health/readiness")
def readiness():
    checks = services.readiness()
    status_code = 200 if all(checks.values()) else 503
    return JSONResponse(status_code=status_code, content={"status": "ready" if status_code == 200 else "not_ready", "checks": checks})

@app.exception_handler(HTTPException)
async def http_error_handler(request: Request, exc: HTTPException):
    code = "NOT_FOUND" if exc.status_code == 404 else "INVALID_REQUEST"
    return JSONResponse(status_code=exc.status_code, content={"error": {"code": code, "message": str(exc.detail), "details": {}}})

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(status_code=400, content={"error": {"code": "INVALID_REQUEST", "message": str(exc), "details": {}}})

@app.exception_handler(Exception)
async def unhandled_error_handler(request: Request, exc: Exception):
    logger.exception("unhandled_request_error")
    return JSONResponse(status_code=500, content={"error": {"code": "SYSTEM_ERROR", "message": "An unexpected system error occurred.", "details": {}}})

frontend_dir = Path(__file__).resolve().parents[1] / "frontend"
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")