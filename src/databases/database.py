from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)
from sqlalchemy.orm import (
    declared_attr,
    Mapped,
    mapped_column,
    declarative_base
)

from configs.config import settings

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
    f"{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/"
    f"{settings.POSTGRES_DB}"
)

class PreBase:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

Base = declarative_base(cls=PreBase)

async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

async_session = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_session():
    async with async_session() as session:
        yield session
