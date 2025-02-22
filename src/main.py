import contextlib
from typing import AsyncIterator

from fastapi import FastAPI
from sqladmin import Admin
from starlette.middleware.cors import CORSMiddleware

from src.admin.admin import UserAdmin, RoleAdmin
from src.admin.auth_admin import authentication_backend
from src.databases.database import db_manager
from src.auth.role import create_roles
from src.auth.user import create_admin_user
from src.api.api import main_router
from src.configs.config import settings


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    db_manager.init(settings.SQLALCHEMY_DATABASE_URL)
    await create_roles()
    await create_admin_user()
    yield
    await db_manager.close()


app = FastAPI(
    title=settings.SERVICE_TITLE,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_router)

admin = Admin(
    app,
    authentication_backend=authentication_backend,
    base_url="/admin",
    title="SERVICE Admin"
)

admin.add_view(UserAdmin)
admin.add_view(RoleAdmin)
