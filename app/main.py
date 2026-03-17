from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.user import Usuario

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "ok"}

@app.get("/usuarios")
async def listar_usuarios(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Usuario))
    return result.scalars().all()