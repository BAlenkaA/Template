from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.configs.loggers import logger
from src.databases.database import db_manager
from src.models.user import Role, User


async def create_roles() -> None:
    """
    Creates roles in the database if they don't exist.
    """
    async with db_manager.session() as session:
        roles_to_create = ["admin", "user"]
        existing_roles = await session.execute(select(Role))

        existing_role_names = [role.name for role in existing_roles.scalars()]

        for role_name in roles_to_create:
            if role_name not in existing_role_names:
                new_role = Role(name=role_name)
                session.add(new_role)
        await session.commit()


async def is_admin(user_id: int, db: AsyncSession) -> bool:
    """
    Checks whether the user is an administrator.
    """
    user = await db.execute(select(User).where(User.id == user_id))
    user_data = user.scalar_one_or_none()

    if not user_data:
        return False

    if user_data.role.name == "admin":
        return True

    return False
