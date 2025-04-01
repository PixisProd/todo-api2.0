import datetime
from enum import StrEnum

from sqlalchemy import String, Boolean, Enum, text, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


class OrmBase(DeclarativeBase):
    pass


class Roles(StrEnum):
    admin = "admin"
    user = "user"

class OrmUser(OrmBase):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    login: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    role: Mapped[Roles] = mapped_column(Enum(Roles), default=Roles.user, server_default=text(f"'{Roles.user}'"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default=text("true"))


class Status(StrEnum):
    pending = "pending"
    done = "done"

class Priority(StrEnum):
    low = "low"
    normal = "normal"
    high = "high"

class OrmTask(OrmBase):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    task_owner_id: Mapped[int] = mapped_column(ForeignKey(column="users.id", ondelete="CASCADE"), nullable=False, index=True)
    task_name: Mapped[str] = mapped_column(String(40), nullable=False)
    task_description: Mapped[str | None] = mapped_column(String(150), nullable=True)
    task_status: Mapped[Status] = mapped_column(Enum(Status), default=Status.pending, server_default=text(f"'{Status.pending}'"), nullable=False, index=True)
    task_priority: Mapped[Priority] = mapped_column(Enum(Priority), default=Priority.normal, server_default=text(f"'{Priority.normal}'"), nullable=False, index=True)
    task_creation_time: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), 
                                                                  default=datetime.datetime.now(datetime.UTC))
    task_last_update_time: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), 
                                                                     default=datetime.datetime.now(datetime.UTC), 
                                                                     onupdate=datetime.datetime.now(datetime.UTC))