from pydantic import BaseModel, Field

from src.models import Status, Priority


class TodoRequest(BaseModel):
    task_name: str = Field(max_length=40, min_length=1)
    task_description: str | None = Field(default=None, max_length=150)
    task_status: Status | None = Field(default=Status.pending)
    task_priority: Priority | None = Field(default=Priority.normal)
