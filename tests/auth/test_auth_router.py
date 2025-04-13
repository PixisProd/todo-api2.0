import pytest
from httpx import AsyncClient
from starlette import status

from src.auth.router import router as auth_router
from src.database import get_db
from src.auth.service import verify_access_token
from src.config import settings
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
async def test_about_user(get_ac: AsyncClient):
    response = await get_ac.get(url=f"{auth_router.prefix}/about")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
        "get_ac",
        [{
            get_db: get_test_db
        }],
        indirect=True
)
@pytest.mark.asyncio
async def test_register_user(get_ac: AsyncClient):
    response = await get_ac.post(
        url=f"{auth_router.prefix}/register",
        json={
            "login": "test_user123",
            "password": "test123",
            "name": "tester123",
            "email": "test123@pixis.com"
        }
    )
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.parametrize(
        "get_ac",
        [{
            get_db: get_test_db
        }],
        indirect=True
)
@pytest.mark.asyncio
async def test_login(get_ac: AsyncClient):
    response = await get_ac.post(
        url=f"{auth_router.prefix}/login",
        data={
            "username": settings.TEST_USER_LOGIN,
            "password": settings.TEST_USER_PASSWORD
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.cookies

@pytest.mark.parametrize(
        "get_ac",
        [{
            verify_access_token: lambda: {"sub": 1}
        }],
        indirect=True
)
@pytest.mark.asyncio
async def test_logout(get_ac: AsyncClient):
    response = await get_ac.post(url=f"{auth_router.prefix}/logout")
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.parametrize(
        "get_ac",
        [{
            get_db: get_test_db
        }],
        indirect=True
)
@pytest.mark.asyncio
async def test_refresh_token(get_ac: AsyncClient):
    refresh_token = await get_ac.post(
        url=f"{auth_router.prefix}/login",
        data={
            "username": settings.TEST_USER_LOGIN,
            "password": settings.TEST_USER_PASSWORD
        }
    )
    refresh_token = refresh_token.cookies.get(settings.JWT_REFRESH_TOKEN_COOKIE_NAME)
    get_ac.cookies={
        settings.JWT_REFRESH_TOKEN_COOKIE_NAME: refresh_token
    }
    response = await get_ac.post(
        url=f"{auth_router.prefix}/refresh-token"
    )
    assert response.status_code == status.HTTP_200_OK