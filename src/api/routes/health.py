"""Health check routes"""

from fastapi import APIRouter
from datetime import datetime
from src.utils.config import get_settings

settings = get_settings()
router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.app_version
    }


@router.get("/health/ready")
async def readiness_check():
    """Readiness check endpoint"""
    # Could add checks for database, external services, etc.
    return {
        "status": "ready",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/health/live")
async def liveness_check():
    """Liveness check endpoint"""
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat()
    }
