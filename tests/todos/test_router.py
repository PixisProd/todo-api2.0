import pytest
import pytest_asyncio
from httpx import AsyncClient

from src.todo.router import router as todo_router
from tests.fixtures import get_ac


@pytest.mark.asyncio
async def test_get_all_user_tasks(get_ac: AsyncClient):
    response = await get_ac.get(url=f"{todo_router.prefix}/tasks")
    print(response.status_code)
    assert response.status_code == 200