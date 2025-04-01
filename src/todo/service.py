from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import OrmTask
from src.todo.schemas import TodoRequest


async def get_all_user_tasks_from_db(user_id: int, db: AsyncSession):
    query = select(OrmTask).where(OrmTask.task_owner_id == user_id)
    result = await db.execute(query)
    return result.scalars().all()


async def add_task_to_db(user_id: int, task: TodoRequest, db: AsyncSession) -> None:
    to_add = OrmTask(**task.model_dump())
    to_add.task_owner_id = user_id
    db.add(to_add)
    try:
        await db.commit()
    except Exception as e:
        print(e)
        await db.rollback()