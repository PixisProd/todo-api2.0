from fastapi import APIRouter, Path
from fastapi.responses import JSONResponse
from starlette import status

from src.auth.dependencies import user_dependency
from src.database import db_dependency
from src.todo.service import get_all_user_tasks_from_db, add_task_to_db, get_user_task, delete_user_task, edit_user_task
from src.todo.schemas import TodoRequest, TodoUpdateRequest


router = APIRouter(
    tags=["Todo Logic 📃"],
    prefix="/todo"
)


@router.get("/tasks", status_code=status.HTTP_200_OK, summary="Get all user tasks")
async def get_all_user_tasks(user: user_dependency, db: db_dependency):
    tasks = await get_all_user_tasks_from_db(user_id=int(user.get('sub')), db=db)
    return tasks


@router.post("/tasks", status_code=status.HTTP_201_CREATED, summary="Create task")
async def add_task_to_user(user: user_dependency, db: db_dependency, todo: TodoRequest):
    task_id = await add_task_to_db(user_id=int(user.get("sub")), task=todo, db=db)
    return {"message": "Task successfully created", "task_id": task_id}


@router.get("/tasks/{task_id}", status_code=status.HTTP_200_OK, summary="Get user task by ID")
async def get_user_task_by_id(user: user_dependency, db: db_dependency, task_id: int = Path(gt=0)):
    task = await get_user_task(user_id=int(user.get("sub")), task_id=task_id, db=db)
    return task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete user task by ID")
async def delete_user_task_by_id(user: user_dependency, db: db_dependency, task_id: int = Path(gt=0)):
    await delete_user_task(user_id=int(user.get("sub")), task_id=task_id, db=db)


@router.put("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Edit user task by ID")
async def edit_user_task_by_id(user: user_dependency, db: db_dependency, to_edit: TodoUpdateRequest, task_id: int = Path(gt=0)):
    await edit_user_task(user_id=int(user.get("sub")), task_id=task_id, db=db, content=to_edit)