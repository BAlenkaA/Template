from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.auth.hash_pass import hash_password
from src.auth.jwt import decode_access_token
from src.auth.role import is_admin
from src.configs.config import settings
from src.databases.database import get_async_session, db_manager
from src.models.user import User, Role

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login-swagger", scheme_name="Bearer")


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_async_session)
) -> User:
    """
    Retrieves the current user from the db.
    """
    try:

        payload = decode_access_token(token)
        username = payload.get("sub")

        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    user = await db.execute(select(User).where(User.username == username))
    user_data = user.scalar_one_or_none()

    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user_data


async def require_admin(
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_session)
) -> None:
    """
    Requires the user to be an administrator.
    """
    if not await is_admin(user.id, db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")


async def create_admin_user() -> None:
    """
    Creates a user with the role of 'admin', if it does not already exist, creates.
    """
    async with db_manager.session() as session:
        admin_role = await session.execute(select(Role).where(Role.name == "admin"))
        role = admin_role.scalar_one_or_none()

        if not role:
            role = Role(name="admin")
            session.add(role)
            await session.commit()
            await session.refresh(role)

        admin_user = await session.execute(
            select(User).where(User.username == "admin")
        )
        user = admin_user.scalar_one_or_none()

        if not user:
            hashed_password = hash_password(settings.ADMIN_PASSWORD)
            user = User(
                username="admin",
                hashed_password=hashed_password,
                role_id=role.id  # noqa
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
