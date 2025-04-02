from typing import List

from fastapi import HTTPException
from starlette import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import OrmTask
from src.todo.schemas import TodoRequest


async def get_all_user_tasks_from_db(user_id: int, db: AsyncSession):
    query = select(OrmTask).where(OrmTask.task_owner_id == user_id)
    result = await db.execute(query)
    return result.scalars().all()


async def get_user_task_by_id_from_db(user_id: int, db: AsyncSession, task_id: int):
    query = select(OrmTask).where(OrmTask.task_owner_id == user_id, OrmTask.id == task_id)
    result = await db.execute(query)
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return task


async def add_task_to_db(user_id: int, task: TodoRequest, db: AsyncSession) -> None:
    to_add = OrmTask(**task.model_dump())
    to_add.task_owner_id = user_id
    db.add(to_add)
    try:
        await db.commit()
    except Exception as e:
        print(e)
        await db.rollback()