from enum import StrEnum

from sqlalchemy import String, Boolean, Enum, text
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
    role: Mapped[Roles] = mapped_column(Enum(Roles), default=Roles.user, server_default=text("'user'"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default=text("true"))