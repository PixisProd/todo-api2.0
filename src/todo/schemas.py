from pydantic import BaseModel, Field

from src.models import Status, Priority


class TodoRequest(BaseModel):
    task_name: str = Field(max_length=40, min_length=1, examples=["Buy milk"])
    task_description: str | None = Field(default=None, max_length=150, examples=["Till midnight"])
    task_status: Status | None = Field(default=Status.pending)
    task_priority: Priority | None = Field(default=Priority.normal, examples=["high"])


class TodoUpdateRequest(TodoRequest):
    task_name: str | None = Field(default=None, max_length=40, min_length=1, examples=["Buy water"])
    task_description: str | None = Field(default=None, max_length=150, examples=["Till dawn"])
    task_status: Status = Field(...)
    task_priority: Priority | None = Field(default=None)
