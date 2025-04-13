import pytest
from pytest import FixtureRequest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from src.main import app
from tests.database import (
    create_test_tables,
    delete_test_tables,
    create_test_user,
    create_test_task
)


@pytest_asyncio.fixture(autouse=True)
async def prepare_databases():
    try:
        await create_test_tables()
        await create_test_user()
        await create_test_task()
        yield
    finally:
        await delete_test_tables()


@pytest_asyncio.fixture(scope="function")
async def get_ac(request: FixtureRequest):
    try:
        app.dependency_overrides = request.param
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            yield ac
    finally:
        app.dependency_overrides.clear()
        
    


        
    
    

