from fastapi import APIRouter, Path
from starlette import status

from src.database import db_dependency
from src.admin.dependencies import admin_dependency
from src.admin.service import deactivate_user, activate_user, get_all_users_from_db, get_all_todos_from_db


router = APIRouter(prefix="/admin")


@router.patch("/{user_id}/deactivate", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_user_by_id(db: db_dependency, _: admin_dependency, user_id: int = Path(gt=0)):
    await deactivate_user(user_id=user_id, db=db)


@router.patch("/{user_id}/activate", status_code=status.HTTP_204_NO_CONTENT)
async def activate_user_by_id(db: db_dependency, _: admin_dependency, user_id: int = Path(gt=0)):
    await activate_user(user_id=user_id, db=db)


@router.get("/users", status_code=status.HTTP_200_OK)
async def get_all_users(db: db_dependency, _: admin_dependency):
    users = await get_all_users_from_db(db=db)
    return users


@router.get("/todos", status_code=status.HTTP_200_OK)
async def get_all_todos(db: db_dependency, _: admin_dependency):
    todos = await get_all_todos_from_db(db=db)
    return todos
