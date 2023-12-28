from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None


class TaskCreate(TaskBase):
    due_date: Optional[datetime] = None
    priority: Optional[int] = None


class Task(TaskBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    completed: bool = False

    class Config:
        json_schema_extra = {"from_orm": True}
