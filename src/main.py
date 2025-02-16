from fastapi import FastAPI

from src.api.api import main_router
from src.configs.config import settings

app = FastAPI(title=settings.SERVICE_TITLE)

app.include_router(main_router)
