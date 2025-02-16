import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent

ENV_FILE_PATH = os.path.join(BASE_DIR, "configs", ".env")

class Settings(BaseSettings):
    SERVICE_TITLE: str = "Service"
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    # SECRET: str = 'SECRET'

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        extra="allow",
    )

settings = Settings()
