from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool

from src.auth.security.bcrypt import bcrypt_context
from src.config import settings
from src.database import OrmBase
from src.models import OrmUser, OrmTask


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


async def create_test_user():
    async with async_test_session_factory() as db:
        to_add = OrmUser(
            login=settings.TEST_USER_LOGIN,
            password=settings.TEST_USER_PASSWORD,
            name=settings.TEST_USER_NAME,
            email=settings.TEST_USER_EMAIL
        )
        to_add.password = bcrypt_context.hash(to_add.password)
        db.add(to_add)
        try:
            await db.commit()
        except Exception as e:
            await db.rollback()
            print(e)


async def create_test_task():
    async with async_test_session_factory() as db:
        to_add = OrmTask(task_name="Test task", task_owner_id=1)
        db.add(to_add)
        try:
            await db.commit()
        except Exception as e:
            await db.rollback()
            print(e)
            