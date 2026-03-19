"""Configuration module for API"""

from dotenv import load_dotenv
import os
from functools import lru_cache

load_dotenv()

class Settings:
    """Application settings from environment variables"""
    
    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/docanalysis")
    DATABASE_POOL_SIZE: int = int(os.getenv("DATABASE_POOL_SIZE", 20))
    DATABASE_MAX_OVERFLOW: int = int(os.getenv("DATABASE_MAX_OVERFLOW", 10))
    
    # Redis/Cache
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CACHE_TTL: int = int(os.getenv("CACHE_TTL_SECONDS", 3600))
    
    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    
    # Vector Database
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "")
    PINECONE_ENVIRONMENT: str = os.getenv("PINECONE_ENVIRONMENT", "us-west1-gcp")
    VECTOR_DIMENSION: int = int(os.getenv("VECTOR_DIMENSION", 1536))
    
    # Security
    JWT_SECRET: str = os.getenv("JWT_SECRET", "change-me-in-production")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    
    # CORS
    ALLOWED_ORIGINS: list = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
    
    # File Upload
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", 50))
    SUPPORTED_EXTENSIONS: list = os.getenv("SUPPORTED_EXTENSIONS", "pdf,docx,txt,png,jpg,jpeg").split(",")
    
    # LLM
    DEFAULT_LLM_MODEL: str = os.getenv("DEFAULT_LLM_MODEL", "gpt-4")
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", 0.7))
    LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", 2000))
    
    # Features
    ENABLE_ASYNC_PROCESSING: bool = os.getenv("ENABLE_ASYNC_PROCESSING", "true").lower() == "true"
    ENABLE_CACHING: bool = os.getenv("ENABLE_CACHING", "true").lower() == "true"
    ENABLE_PROMETHEUS: bool = os.getenv("ENABLE_PROMETHEUS", "true").lower() == "true"
    
    # Monitoring
    SENTRY_DSN: str = os.getenv("SENTRY_DSN", "")

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
