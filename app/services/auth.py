from fastapi import Depends, HTTPException, status, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.models.user import User
from app.schemas.auth import UserLogin
from app.core.security import verify_password, create_access_token
from app.core.security import oauth2_scheme, decode_token
from datetime import timedelta
from app.core.settings import settings
from app.core.errors import SIN_CREDENCIALES

async def authenticate_user(auth_data: UserLogin, db: AsyncSession, response: Response):
    result = await db.execute(
        select(User).where(User.username == auth_data.username)
    )

    user = result.scalar_one_or_none()

    if not user:
        raise SIN_CREDENCIALES

    if not verify_password(auth_data.password, user.passwordHash):
        raise SIN_CREDENCIALES
    
    access_token = create_access_token(
        data={"sub": user.id, "role": user.role.value, "username": user.username, "type": "access"},
        expires_delta=timedelta(minutes=30)
    )

    refresh_token = create_access_token(
        data={"sub": user.id, "role": user.role.value, "username": user.username, "type": "refresh"},
        expires_delta=timedelta(days=7)
    )

    response.set_cookie(
            key=settings.ACCESS_COOKIE_NAME,
            value=access_token,
            httponly=True,
            max_age=3600,
            expires=3600,
            samesite="lax",
            secure=False,
            path="/",
        )
    
    response.set_cookie(
            key=settings.REFRESH_COOKIE_NAME,
            value=refresh_token,
            httponly=True,
            max_age=3600,
            expires=3600,
            samesite="lax",
            secure=False,
            path="/auth/refresh",
        )

    return {settings.ACCESS_COOKIE_NAME: access_token, "token_type": "bearer"}

async def refresh_tokens(auth_data: UserLogin, db: AsyncSession, response: Response):
    pass

async def _create_cookies():
    pass