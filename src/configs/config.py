import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent

ENV_FILE_PATH = os.path.join(BASE_DIR, "configs", ".env")

class Settings(BaseSettings):
    # Service
    SERVICE_TITLE: str = "Service"
    # Postgres
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    # Users
    SECRET_KEY: str = "Secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    # Admin
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str
    # Logger
    LOG_FILE: str = "/logs/service.log"
    LOG_LEVEL: str = "DEBUG"

    @property
    def SQLALCHEMY_DATABASE_URL(self):
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        extra="allow",
    )

settings = Settings()
