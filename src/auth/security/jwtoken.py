import datetime

import jwt
from fastapi import HTTPException
from starlette import status

from src.config import settings


ACCESS_TOKEN_LIFETIME = datetime.timedelta(minutes=60)
REFRESH_TOKEN_LIFETIME = datetime.timedelta(days=7)


def create_token(user_id: int, now: datetime.datetime, lifetime: datetime.timedelta, payload: dict = None) -> str:
    temp_payload = {"sub": str(user_id),
                    "exp": now + lifetime,
                    "iat": now}
    if payload:
        temp_payload.update(payload)
    return jwt.encode(temp_payload, key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_access_token(user_id: int, payload: dict, now: datetime.datetime) -> str:
    return create_token(user_id=user_id, now=now, lifetime=ACCESS_TOKEN_LIFETIME, payload=payload)


def create_refresh_token(user_id: int, now: datetime.datetime) -> str:
    return create_token(user_id=user_id, now=now, lifetime=REFRESH_TOKEN_LIFETIME)