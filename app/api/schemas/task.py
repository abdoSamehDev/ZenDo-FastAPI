from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None


class TaskCreate(TaskBase):
    due_date: Optional[datetime] = None
    priority: Optional[int] = None


class TaskUpdate(TaskBase):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[int] = None
    completed: bool = False
    updated_at: datetime = datetime.utcnow()


class Task(TaskBase):
    id: int
    user_id: int
    due_date: Optional[datetime] = None
    priority: Optional[int] = None
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        json_schema_extra = {"from_orm": True}
