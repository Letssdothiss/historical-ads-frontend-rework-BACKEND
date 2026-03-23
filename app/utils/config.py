"""
Configuration settings for the Historical Ads Backend
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    HISTORICAL_API_BASE_URL: str = "https://historical.api.jobtechdev.se"
    API_TIMEOUT: int = 30
    API_MAX_RETRIES: int = 3
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 10
    MAX_PAGE_SIZE: int = 100
    
    # Export
    MAX_EXPORT_RECORDS: int = 10000
    
    # App
    APP_NAME: str = "Historical Ads Backend API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # CORS
    CORS_ORIGINS: list[str] = ["*"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()