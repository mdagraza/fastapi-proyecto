import typer
from faker import Faker # https://pypi.org/project/Faker/

import asyncio
from app.db.database import AsyncSessionLocal

from app.models.report import Report, ReportPriority, ReportCategory
from app.schemas.report import ReportCreate, ReportCategoryCreate
from app.schemas.user import UserCreate
from app.models.user import User

from app.core.security import hash_password
from app.core.settings import settings

cli = typer.Typer()
faker = Faker()

@cli.callback()
def main():
    pass

@cli.command(help="Genera reports de prueba, con usuarios y categorías") #uv run python -m scripts.manage reports --n 5 
def reports(n: int = 5):
    print(f"Generando {n} reports de prueba...")
    asyncio.run(_create_reports(n))

async def _create_user():
    async with AsyncSessionLocal() as db:
        user_data = UserCreate(
            username=faker.user_name(),
            email=faker.email(),
            password=hash_password(settings.ADMIN_PASSWORD), #Se usa la misma contraseña de admin para los usuarios de prueba
        )
        new_user = User(**user_data.model_dump())
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return new_user.id

async def _create_category():
    async with AsyncSessionLocal() as db:
        category_data = ReportCategoryCreate(
            name=faker.word(),
            description=faker.sentence(nb_words=5)
        )
        new_category = ReportCategory(**category_data.model_dump())
        db.add(new_category)
        await db.commit()
        await db.refresh(new_category)

        return new_category.id

async def _create_reports(n: int):
    user_id = await _create_user()
    category_id = await _create_category()
    async with AsyncSessionLocal() as db:
        for _ in range(n):
            report_data = ReportCreate(
                title=faker.text(max_nb_chars=30),
                description=faker.paragraph(),
                latitude=faker.latitude(),
                longitude=faker.longitude(),
                priority=faker.random_element(elements=ReportPriority),
                categoryId=category_id,
                userId=user_id
            )
            new_report = Report(**report_data.model_dump())
            db.add(new_report)

        await db.commit()

if __name__ == "__main__":
    cli()