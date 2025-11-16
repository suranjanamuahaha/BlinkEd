```python
"""Application configuration."""
from typing import List


class Settings(BaseSettings):
    """Application settings."""
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "BlinkEd"
    
    # Database
    DATABASE_URL: str
    
    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Google APIs
    GOOGLE_GEMINI_API_KEY: str
    GOOGLE_TTS_CREDENTIALS_PATH: str = ""
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/1"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    # File Storage
    MAX_FILE_SIZE_MB: int = 500
    UPLOAD_DIR: str = "./uploads"
    CACHE_DIR: str = "./cache"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


"""
Archived configuration for the legacy FastAPI backend.

This file is a placeholder. The active backend is now the Django project
under `Backend/django_auth`. If you need to restore the FastAPI config, add
the original settings back and ensure the required dependencies are installed.
"""

__all__ = []
