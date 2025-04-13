from fastapi import APIRouter, Depends, Cookie, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from src.database import db_dependency
from src.auth.schemas import UserRegistration
from src.auth.service import register_user, validate_user, refresh_access_token, get_user
from src.config import settings
from src.auth.dependencies import user_dependency


router = APIRouter(
    prefix="/auth",
    tags=["Auth 🔐"]
)


@router.get("/about", status_code=status.HTTP_200_OK, summary="Get info about user")
async def about_user(db: db_dependency, user: user_dependency):
    info = await get_user(user_id=int(user.get("sub")), db=db)
    return info


@router.post("/register", status_code=status.HTTP_201_CREATED, summary="Registration endpoint")
async def register(body: UserRegistration, db: db_dependency):
    await register_user(data=body, db=db)
    return JSONResponse(content={"message": "User successfully created"}, status_code=status.HTTP_201_CREATED)


@router.post("/login", status_code=status.HTTP_200_OK, summary="Login endpoint")
async def login(db: db_dependency, credentials: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)):
    access_token, refresh_token = await validate_user(credentials=credentials, db=db)
    response = JSONResponse(content={"message": "Successful login"}, status_code=status.HTTP_200_OK)
    response.set_cookie(key=settings.JWT_ACCESS_TOKEN_COOKIE_NAME, value=access_token, httponly=True)
    response.set_cookie(key=settings.JWT_REFRESH_TOKEN_COOKIE_NAME, value=refresh_token, httponly=True)
    return response


@router.post("/logout", status_code=status.HTTP_200_OK, summary="Log out from account")
async def logout(_: user_dependency):
    response = JSONResponse(content={"message": f"Successfully logout"})
    response.delete_cookie(key=settings.JWT_ACCESS_TOKEN_COOKIE_NAME)
    response.delete_cookie(key=settings.JWT_REFRESH_TOKEN_COOKIE_NAME)
    return response


@router.post("/refresh-token", status_code=status.HTTP_200_OK, summary="Refresh access token endpoint")
async def refresh_token(db: db_dependency, refresh_token: str = Cookie(default=None, alias=settings.JWT_REFRESH_TOKEN_COOKIE_NAME)):
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Refresh token missing")
    new_access_token = await refresh_access_token(db=db, refresh_token=refresh_token)
    response = JSONResponse(content={"message": "Token successfully refreshed"}, status_code=status.HTTP_200_OK)
    response.set_cookie(key=settings.JWT_ACCESS_TOKEN_COOKIE_NAME, value=new_access_token, httponly=True)
    return response