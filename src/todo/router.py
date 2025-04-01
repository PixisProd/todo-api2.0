from fastapi import APIRouter
from fastapi.responses import JSONResponse
from starlette import status

from src.auth.dependencies import user_dependency
from src.database import db_dependency
from src.todo.service import get_all_user_tasks_from_db, add_task_to_db
from src.todo.schemas import TodoRequest


router = APIRouter(
    prefix="/todo"
)


@router.get("/tasks", status_code=status.HTTP_200_OK)
async def get_all_user_tasks(user: user_dependency, db: db_dependency):
    tasks = await get_all_user_tasks_from_db(user_id=int(user.get('sub')), db=db)
    return tasks

# Stopped here, tomorrow start from here
@router.post("/tasks", status_code=status.HTTP_201_CREATED)
async def add_task_to_user(user: user_dependency, db: db_dependency, todo: TodoRequest):
    await add_task_to_db(user_id=int(user.get("sub")), task=todo, db=db)