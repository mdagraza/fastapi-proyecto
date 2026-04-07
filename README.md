# Proyecto de FastAPI

API REST construida con **FastAPI** usando **SQLAlchemy async** con **PostgreSQL**.

## Descripción

Este proyecto expone una API con FastAPI que:

- Inicia un admin por defecto usando seeds.
- Expone rutas básicas (como `/reports`). Más info en `/docs`.
- Utiliza base de datos PostgreSQL configurada mediante variables de entorno.

---

## 1. Preparar el entorno

El proyecto usa **uv**, por lo que puedes crear el entorno virtual y sincronizar dependencias con un solo comando:

```bash
uv sync
```

Esto creará `.venv` e instalará todas las dependencias automáticamente.

## 2. Configurar variables de entorno

Copia el archivo de ejemplo y edítalo con tus datos

```bash
cp .env.example .env
```

Ejemplo de .env

```markdown
DATABASE_URL=postgresql+asyncpg://usuario:contraseña@localhost:5432/nombre_db

ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@dominio.com
ADMIN_PASSWORD=contraseña_segura

SECRET_KEY=EstoEsUnaClaveSecretaMuySegura0123456789
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
ACCESS_COOKIE_NAME=t_access
REFRESH_COOKIE_NAME=t_refresh

BACKEND_CORS_ORIGINS=["http://ejemplo.com", "https://ejemplo.com"]
```

## 3. Preparar la Base de Datos

```bash
uv run alembic upgrade head
```

## 4. Ejecutar la API

```bash
uv run uvicorn app.main:app --reload
```
