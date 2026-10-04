from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from app.backend.routes import router

app = FastAPI(
    title="Clinical AI Evaluation Lab",
    version="0.4.0",
    description="API for the CAIEL clinical AI evaluation platform.",
)

app.include_router(router, prefix="/api/v1")


@app.exception_handler(HTTPException)
async def http_error_handler(request: Request, exc: HTTPException):
    code = "NOT_FOUND" if exc.status_code == 404 else "INVALID_REQUEST"
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": code, "message": str(exc.detail), "details": {}}},
    )


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"error": {"code": "INVALID_REQUEST", "message": str(exc), "details": {}}},
    )


@app.exception_handler(Exception)
async def unhandled_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": {"code": "SYSTEM_ERROR", "message": "An unexpected system error occurred.", "details": {}}},
    )
