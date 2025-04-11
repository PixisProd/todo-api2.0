import pytest
import pytest_asyncio
from httpx import AsyncClient

from src.auth.service import verify_access_token
from src.database import get_db
from src.todo.router import router as todo_router
from tests.database import get_test_db

@pytest.mark.parametrize(
        "get_ac",
        [{
            get_db: get_test_db,
            verify_access_token: lambda: {"sub": 1}
        }],
        indirect=True
)
@pytest.mark.asyncio
async def test_get_all_user_tasks(get_ac: AsyncClient):
    response = await get_ac.get(url=f"{todo_router.prefix}/tasks")
    print(response.json())
    assert response.status_code == 200