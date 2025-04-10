from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool

from src.config import settings
from src.database import OrmBase


TEST_DATABASE_URL: str = f"postgresql+asyncpg://{settings.PG_USER}:{settings.PG_PASSWORD}@{settings.PG_HOST}/{settings.PG_TEST_DATABASE_NAME}"


async_test_engine = create_async_engine(
    url=TEST_DATABASE_URL,
    future=True,
    echo=False,
    poolclass=NullPool
)


async_test_session_factory = async_sessionmaker(
    bind=async_test_engine,
    expire_on_commit=False
)


async def get_test_db():
    async with async_test_session_factory() as db:
        yield db


async def create_test_tables():
    async with async_test_engine.begin() as conn:
        await conn.run_sync(fn=OrmBase.metadata.create_all)


async def delete_test_tables():
    async with async_test_engine.begin() as conn:
        await conn.run_sync(fn=OrmBase.metadata.drop_all)