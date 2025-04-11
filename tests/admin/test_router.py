import pytest
from httpx import AsyncClient
from starlette import status

from src.database import get_db
from src.admin.service import verify_admin
from src.admin.router import router as admin_router
from tests.database import get_test_db


@pytest.mark.parametrize(
        "get_ac",
        [{
            get_db: get_test_db,
            verify_admin: lambda: {"role": "admin"}
        }],
        indirect=True
)
@pytest.mark.asyncio
async def test_get_all_users(get_ac: AsyncClient):
    response = await get_ac.get(url=f"{admin_router.prefix}/users")
    assert response.status_code == status.HTTP_200_OK