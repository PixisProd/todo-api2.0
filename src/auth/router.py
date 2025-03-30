from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from src.database import db_dependency
from src.auth.schemas import UserRegistration
from src.auth.service import register_user, validate_user


router = APIRouter(prefix="/auth")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(body: UserRegistration, db: db_dependency):
    await register_user(data=body, db=db)
    return JSONResponse(content={"detail": "User successfully created"}, status_code=status.HTTP_201_CREATED)


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(db: db_dependency, credentials: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)):
    return await validate_user(credentials, db=db)
