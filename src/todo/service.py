from fastapi import HTTPException
from starlette import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import OrmTask
from src.todo.schemas import TodoRequest, TodoUpdateRequest


TODO_NOT_FOUND_EXCEPTION_TEXT = "Todo not found"


async def get_all_user_tasks_from_db(user_id: int, db: AsyncSession):
    query = select(OrmTask).where(OrmTask.task_owner_id == user_id)
    result = await db.execute(query)
    return result.scalars().all()


async def get_user_task(user_id: int, db: AsyncSession, task_id: int):
    query = select(OrmTask).where(OrmTask.task_owner_id == user_id, OrmTask.id == task_id)
    result = await db.execute(query)
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return task


async def add_task_to_db(user_id: int, task: TodoRequest, db: AsyncSession) -> int:
    to_add = OrmTask(**task.model_dump())
    to_add.task_owner_id = user_id
    db.add(to_add)
    try:
        await db.flush()
        await db.commit()
    except Exception as e:
        print(e)
        await db.rollback()
    return to_add.id


async def delete_user_task(user_id: int, task_id: int, db:AsyncSession) -> None:
    query = select(OrmTask).where(OrmTask.task_owner_id == user_id, OrmTask.id == task_id)
    result = await db.execute(query)
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=TODO_NOT_FOUND_EXCEPTION_TEXT)
    await db.delete(task)
    await db.commit()
        
    
async def edit_user_task(user_id: int, task_id: int, db: AsyncSession, content: TodoUpdateRequest) -> None:
    query = select(OrmTask).where(OrmTask.task_owner_id == user_id, OrmTask.id == task_id)
    result = await db.execute(query)
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=TODO_NOT_FOUND_EXCEPTION_TEXT)
    task.task_status = content.task_status
    if content.task_name is not None:
        task.task_name = content.task_name
    if content.task_description is not None:
        task.task_description = content.task_description
    if content.task_priority is not None:
        task.task_priority = content.task_priority
    await db.commit()
