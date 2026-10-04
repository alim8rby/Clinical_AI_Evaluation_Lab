from fastapi import APIRouter
from app.backend.settings import settings

router = APIRouter()

@router.get("/health")
def health() -> dict:
    return {"status":"ok","environment":settings.app_env,"version":"0.4.0"}
