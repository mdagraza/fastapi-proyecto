from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.models.user import User
from app.core.security import oauth2_scheme, decode_token
from app.core.settings import settings
from app.core.errors import NO_AUTENTICADO

async def get_current_user(request: Request, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    if not token: #TODO: Separar esta logica para que no se repita en cada endpoint protegido (dependencies/auth.py)
        cookie_token = request.cookies.get(settings.ACCESS_COOKIE_NAME)
        if cookie_token:
            token = cookie_token
        else:
            raise NO_AUTENTICADO
    
    payload = await decode_token(token) 

    if payload is None:
        raise NO_AUTENTICADO
     
    user_id = payload.get("sub")
    
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    
    user = result.scalar_one_or_none()

    if not user:
        raise NO_AUTENTICADO
    
    return user