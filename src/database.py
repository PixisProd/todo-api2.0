from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.config import settings
from src.models import OrmBase


DATABASE_URL: str = f"postgresql+asyncpg://{settings.PG_USER}:{settings.PG_PASSWORD}@{settings.PG_HOST}/{settings.PG_DATABASE_NAME}"


async_engine = create_async_engine(url=DATABASE_URL, future=True, echo=False)


async_session_factory = async_sessionmaker(bind=async_engine, expire_on_commit=False)


async def get_db():
    async with async_session_factory() as session:
        yield session


db_dependency = Annotated[AsyncSession, Depends(get_db)]


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(fn=OrmBase.metadata.create_all)


async def delete_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(fn=OrmBase.metadata.drop_all)