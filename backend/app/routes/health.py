"""
Health check endpoints
"""
from fastapi import APIRouter
from app.schemas import HealthResponse
from app.config import settings

router = APIRouter()

@router.get("", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    """
    try:
        from redis import Redis
        redis_conn = Redis.from_url(settings.REDIS_URL)
        redis_connected = redis_conn.ping()
    except:
        redis_connected = False
    
    try:
        from app.database import engine
        database_connected = engine.raw_connection().connection.ping()
    except:
        database_connected = False
    
    return HealthResponse(
        status="healthy",
        redis_connected=redis_connected,
        database_connected=database_connected,
        version=settings.APP_VERSION
    )
