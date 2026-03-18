import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User, UserRole
from app.core.security import hash_password

load_dotenv()

async def seed_admin(db: AsyncSession) -> None:
    username = os.getenv("ADMIN_USERNAME")
    email = os.getenv("ADMIN_EMAIL")
    password = os.getenv("ADMIN_PASSWORD")

    result = await db.execute(select(User).where(User.username == username))
    if result.scalar_one_or_none():
        return

    admin = User(
        username=username,
        email=email,
        passwordHash=hash_password(password),
        role=UserRole.admin,
        isActive=True,
    )

    db.add(admin)
    await db.commit()
    print("Admin creado")