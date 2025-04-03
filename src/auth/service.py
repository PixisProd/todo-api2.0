import datetime

import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from src.models import OrmUser
from src.auth.schemas import UserRegistration
from src.auth.security.bcrypt import bcrypt_context
from src.auth.security.jwtoken import create_access_token, create_refresh_token
from src.config import settings


ACCESS_TOKEN_PAYLOAD_EMAIL_KEY = "email"
ACCESS_TOKEN_PAYLOAD_ROLE_KEY = "role"


async def register_user(data: UserRegistration, db: AsyncSession) -> None:
    data.password = bcrypt_context.hash(data.password)
    db.add(OrmUser(**data.model_dump()))
    try:
        await db.flush()
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This user already exists in the system.")


async def validate_user(credentials: OAuth2PasswordRequestForm, db: AsyncSession):
    query = select(OrmUser).where(OrmUser.login == credentials.username)
    result = await db.execute(statement=query)
    user = result.scalar_one_or_none()
    if not user or not bcrypt_context.verify(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect login or password")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Your account has been deactivated")
    now = datetime.datetime.now(datetime.UTC)
    access_token = create_access_token(user_id=user.id, payload={ACCESS_TOKEN_PAYLOAD_EMAIL_KEY: user.email, ACCESS_TOKEN_PAYLOAD_ROLE_KEY: user.role}, now=now)
    refresh_token = create_refresh_token(user_id=user.id, now=now)
    return access_token, refresh_token


async def verify_access_token(token: str = Cookie(None, alias=settings.JWT_ACCESS_TOKEN_COOKIE_NAME)) -> dict:
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing access token")
    try:
        payload = jwt.decode(jwt=token, key=settings.JWT_SECRET_KEY, algorithms=settings.JWT_ALGORITHM)
        return payload
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


async def refresh_access_token(db: AsyncSession, refresh_token: str) -> str:
    try:
        payload: dict = jwt.decode(jwt=refresh_token, key=settings.JWT_SECRET_KEY, algorithms=settings.JWT_ALGORITHM)
        query = select(OrmUser).where(OrmUser.id == int(payload.get("sub")))
        result = await db.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The user does not exist")
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User blocked")
        now = datetime.datetime.now(datetime.UTC)
        new_access_token = create_access_token(user_id=user.id, payload={ACCESS_TOKEN_PAYLOAD_EMAIL_KEY: user.email, ACCESS_TOKEN_PAYLOAD_ROLE_KEY: user.role}, now=now)
        return new_access_token
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired, please re-login")
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
