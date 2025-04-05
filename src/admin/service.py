from fastapi import HTTPException, Cookie
from starlette import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import OrmUser, OrmTask
from src.auth.service import verify_access_token, ACCESS_TOKEN_PAYLOAD_ROLE_KEY
from src.config import settings
from src.models import Roles
from src.auth.service import get_user


async def deactivate_user(user_id: int, db: AsyncSession) -> None:
    user = await get_user(user_id=user_id, db=db)
    if user.role is Roles.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Can't deactivate other admin")
    user.is_active = False
    try:
        await db.commit()
    except Exception as e:
        print(e)
        await db.rollback()


async def activate_user(user_id: int, db: AsyncSession) -> None:
    user = await get_user(user_id=user_id, db=db)
    if user.role is Roles.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Can't activate other admin")
    user.is_active = True
    try:
        await db.commit()
    except Exception as e:
        print(e)
        await db.rollback()


async def verify_admin(token: str = Cookie(None, alias=settings.JWT_ACCESS_TOKEN_COOKIE_NAME)) -> dict:
    payload = await verify_access_token(token=token)
    role = payload.get(ACCESS_TOKEN_PAYLOAD_ROLE_KEY)
    if role != Roles.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Missing admin privileges")
    return payload


async def get_all_users_from_db(db: AsyncSession):
    query = select(OrmUser)
    result = await db.execute(query)
    users = result.scalars().all()
    return users


async def get_all_todos_from_db(db: AsyncSession):
    query = select(OrmTask)
    result = await db.execute(query)
    todos = result.scalars().all()
    return todos