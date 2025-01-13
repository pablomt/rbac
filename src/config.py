from typing import List
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # API Settings
    API_VERSION: str = "1.0.0"
    API_TITLE: str = "Auth Service"
    API_PREFIX: str = "/api"
    DEBUG: bool = False

    # CORS Settings
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    ALLOWED_METHODS: List[str] = ["*"]
    ALLOWED_HEADERS: List[str] = ["*"]

    # AWS Settings
    AWS_REGION: str = "us-east-1"
    COGNITO_CLIENT_ID: str
    COGNITO_CLIENT_SECRET: str
    COGNITO_USER_POOL_ID: str

    # Database Settings
    DATABASE_URL: str
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
