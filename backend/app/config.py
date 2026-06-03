"""
O.R.E Configuration Settings
"""
import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application settings"""
    
    # App
    APP_NAME: str = "O.R.E - AI Workforce Platform"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = os.getenv("DEBUG", "True") == "True"
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "sqlite:///./ore.db"
    )
    
    # Redis / Job Queue
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    RQ_QUEUE_NAME: str = os.getenv("RQ_QUEUE_NAME", "default")
    
    # API
    API_PREFIX: str = "/api"
    CORS_ORIGINS: List[str] = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:8080",
    ]
    
    # Storage
    STORAGE_PATH: str = os.getenv("STORAGE_PATH", "./storage")
    MAX_UPLOAD_SIZE: int = 500 * 1024 * 1024  # 500MB
    
    # FFmpeg
    FFMPEG_PATH: str = os.getenv("FFMPEG_PATH", "ffmpeg")
    FFPROBE_PATH: str = os.getenv("FFPROBE_PATH", "ffprobe")
    
    # Task Processing
    TASK_TIMEOUT: int = int(os.getenv("TASK_TIMEOUT", "3600"))  # 1 hour
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    
    # Agents
    AGENT_TIMEOUT: int = int(os.getenv("AGENT_TIMEOUT", "300"))  # 5 minutes
    
    # Paths
    UPLOAD_DIR: str = os.path.join(STORAGE_PATH, "uploads")
    OUTPUT_DIR: str = os.path.join(STORAGE_PATH, "outputs")
    TEMP_DIR: str = os.path.join(STORAGE_PATH, "temp")
    
    def __init__(self):
        """Create necessary directories"""
        for directory in [self.UPLOAD_DIR, self.OUTPUT_DIR, self.TEMP_DIR]:
            os.makedirs(directory, exist_ok=True)

settings = Settings()
