# app/api/crud/task.py

from sqlalchemy.orm import Session
from app.api.database.models.task import Task
from app.api.schemas.task import TaskCreate
from datetime import datetime


def create_task(db: Session, task: TaskCreate, user_id: int):
    # Placeholder function for creating a task in the database
    task_data = task.model_dump()
    task_data["user_id"] = user_id
    task_data["updated_at"] = datetime.utcnow()
    # task_data["user_id"] = user_id
    db_task = Task(**task_data)
    # db_task["user_id"] = user_id
    print("TASK", db_task)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task(db: Session, task_id: int):
    # Placeholder function for retrieving a task by ID from the database
    return db.query(Task).filter(Task.id == task_id).first()


def update_task(db: Session, task_id: int, task: TaskCreate):
    # Placeholder function for updating a task in the database
    db_task = db.query(Task).filter(Task.id == task_id).first()
    for key, value in task.model_dump().items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int):
    # Placeholder function for deleting a task from the database
    db.query(Task).filter(Task.id == task_id).delete()
    db.commit()
