from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.models.user import User
from app.core.security import oauth2_scheme, decode_token
from app.core.settings import settings
from app.core.errors import NO_AUTENTICADO

async def get_current_user(request: Request, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    payload = await _get_token_payload(request, token)

    user = await _get_user_from_payload(payload.get("sub"), db)
    
    return user

async def get_current_user_jti(request: Request, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    payload = await _get_token_payload(request, token)

    user = await _get_user_from_payload(payload.get("sub"), db)
    
    return user, payload.get("jti")

#Auxiliar
async def _get_token_payload(request: Request, token: str | None = None):
    if not token: 
        cookie_token = request.cookies.get(settings.ACCESS_COOKIE_NAME)
        if cookie_token:
            token = cookie_token
        else:
            raise NO_AUTENTICADO
        
    return decode_token(token)

async def _get_user_from_payload(user_id: str, db: AsyncSession):   
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    
    user = result.scalar_one_or_none()

    if not user:
        raise NO_AUTENTICADO
    
    return user