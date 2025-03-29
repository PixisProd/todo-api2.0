from sqlalchemy.ext.asyncio import AsyncSession

from src.models import OrmUser
from src.auth.schemas import UserRegistration


async def register_user(data: UserRegistration, db: AsyncSession) -> None:
    db.add(OrmUser(**data.model_dump()))
    await db.commit()