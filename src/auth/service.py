from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from src.models import OrmUser
from src.auth.schemas import UserRegistration
from src.auth.security.bcrypt import bcrypt_context


async def register_user(data: UserRegistration, db: AsyncSession) -> None:
    data.password = bcrypt_context.hash(data.password)
    db.add(OrmUser(**data.model_dump()))
    await db.commit()


async def validate_user(credentials: OAuth2PasswordRequestForm, db: AsyncSession) -> OrmUser:
    query = select(OrmUser).where(OrmUser.login == credentials.username)
    result = await db.execute(statement=query)
    user = result.scalar_one_or_none()
    if not user or not bcrypt_context.verify(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect login or password")
    return user


    