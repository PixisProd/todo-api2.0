import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from src.models import OrmUser
from src.auth.schemas import UserRegistration
from src.auth.security.bcrypt import bcrypt_context
from src.auth.security.jwtoken import create_access_token, create_refresh_token


async def register_user(data: UserRegistration, db: AsyncSession) -> None:
    data.password = bcrypt_context.hash(data.password)
    db.add(OrmUser(**data.model_dump()))
    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This user already exists in the system.")


async def validate_user(credentials: OAuth2PasswordRequestForm, db: AsyncSession) -> dict:
    query = select(OrmUser).where(OrmUser.login == credentials.username)
    result = await db.execute(statement=query)
    user = result.scalar_one_or_none()
    if not user or not bcrypt_context.verify(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect login or password")
    now = datetime.datetime.now(datetime.UTC)
    access_token = create_access_token(user_id=user.id, payload={"email": user.email, "role": user.role}, now=now)
    refresh_token = create_refresh_token(user_id=user.id, now=now)
    return {"a": access_token, "r": refresh_token}


    