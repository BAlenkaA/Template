from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.api.validators import validate_user
from src.auth.hash_pass import hash_password, verify_password
from src.auth.user import get_current_user
from src.databases.database import get_async_session
from src.models.user import User, Role
from src.schemas.user import UserRegister, Token, UserLogin, ChangePassword, UserProfile

router = APIRouter()

@router.post("/register", response_model=dict, name="Register new user")
async def register_user(user: UserRegister, db: AsyncSession = Depends(get_async_session)):
    """
    Registration user. \n\n
    Validate user credentials: \n
        - username min length (3 characters)\n
        - password min (8 characters, uppercase, lowercase, special characters (!@#$%^&*_))
    """
    existing_user = await db.execute(User.__table__.select().where(User.username == user.username))

    if existing_user.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    hashed_password = hash_password(user.password)
    new_user = User(
        username=user.username,
        hashed_password=hashed_password,
    )
    user_role = await db.execute(select(Role).where(Role.name == "user"))
    role = user_role.scalar_one_or_none()

    if role:
        new_user.role_id = role.id

    db.add(new_user)
    await db.commit()

    return {"message": "User registered successfully"}


@router.post("/login", response_model=Token, name="Login user")
async def login_user(
        user: UserLogin,
        db: AsyncSession = Depends(get_async_session)
):
    """
    Authorization user.
    Please use the login-swagger endpoint for authorization in swagger.
    """
    access_token = await validate_user(user, db)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login-swagger", include_in_schema=False)
async def login_user(
        user: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: AsyncSession = Depends(get_async_session)
):
    """
    Authorization user in swagger.
    """
    access_token = await validate_user(
        UserLogin(username=user.username, password=user.password),
        db
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserProfile, name="User profile(Auth only)")
async def user_profile(user: User = Depends(get_current_user)):
    """
    Get user profile.
    """
    return {
        "username": user.username,
        "role": user.role.name
    }


@router.post("/change_password", response_model=dict, name="Change password(Auth only)")
async def change_password(
        data: ChangePassword,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_session),
):
    """
    Change user password. \n\n
        - new_password min (8 characters, uppercase, lowercase, special characters (!@#$%^&*_))
    """
    if not verify_password(data.old_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect old password"
        )

    user.hashed_password = hash_password(data.new_password)
    await db.commit()

    return {"message": "Password updated successfully"}
