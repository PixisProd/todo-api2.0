from fastapi import APIRouter, Path
from starlette import status

from src.auth.dependencies import user_dependency
from src.database import db_dependency
from src.todo.service import get_all_user_tasks_from_db, add_task_to_db, get_user_task_by_id_from_db
from src.todo.schemas import TodoRequest


router = APIRouter(
    tags=["Todo Logic 📃"],
    prefix="/todo"
)


@router.get("/tasks", status_code=status.HTTP_200_OK)
async def get_all_user_tasks(user: user_dependency, db: db_dependency):
    tasks = await get_all_user_tasks_from_db(user_id=int(user.get('sub')), db=db)
    return tasks


@router.post("/tasks", status_code=status.HTTP_201_CREATED)
async def add_task_to_user(user: user_dependency, db: db_dependency, todo: TodoRequest):
    await add_task_to_db(user_id=int(user.get("sub")), task=todo, db=db)


@router.get("/tasks/{task_id}")
async def get_user_task_by_id(user: user_dependency, db: db_dependency, task_id: int = Path(gt=0)):
    task = await get_user_task_by_id_from_db(user_id=int(user.get("sub")), task_id=task_id, db=db)
    return task