import pytest
import pytest_asyncio
from httpx import AsyncClient
from starlette import status

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
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
        "get_ac",
        [{
            get_db: get_test_db,
            verify_access_token: lambda: {"sub": 1}
        }],
        indirect=True
)
@pytest.mark.asyncio
async def test_add_task_to_user(get_ac: AsyncClient):
    response = await get_ac.post(
        url=f"{todo_router.prefix}/tasks",
        json={
            "task_name": "Test task"
        }
    )
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.parametrize(
        "get_ac",
        [{
            get_db: get_test_db,
            verify_access_token: lambda: {"sub": 1}
        }],
        indirect=True
)
@pytest.mark.asyncio
async def test_get_user_task_by_id(get_ac: AsyncClient):
    response = await get_ac.get(url=f"{todo_router.prefix}/tasks/1")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
        "get_ac",
        [{
            get_db: get_test_db,
            verify_access_token: lambda: {"sub": 1}
        }],
        indirect=True
)
@pytest.mark.asyncio
async def test_delete_user_task_by_id(get_ac: AsyncClient):
    response = await get_ac.delete(url=f"{todo_router.prefix}/tasks/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.parametrize(
        "get_ac",
        [{
            get_db: get_test_db,
            verify_access_token: lambda: {"sub": 1}
        }],
        indirect=True
)
@pytest.mark.asyncio
async def test_edit_user_task_by_id(get_ac: AsyncClient):
    response = await get_ac.put(
        url=f"{todo_router.prefix}/tasks/1",
        json={"task_status": "done"}
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT