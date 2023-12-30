# app/api/crud/task.py

from sqlalchemy.orm import Session
from app.api.database.models.task import Task
from app.api.schemas.task import TaskCreate, TaskUpdate
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


def get_all_tasks(db: Session, user_id: int):
    # Placeholder function for retrieving all tasks by UserID from the database
    return db.query(Task).filter(Task.user_id == user_id).all()


def get_task(db: Session, task_id: int):
    # Placeholder function for retrieving a task by ID from the database
    return db.query(Task).filter(Task.id == task_id).first()


def update_task(db: Session, task_id: int, task_update: TaskUpdate):
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    for key, value in task_update.model_dump(exclude_unset=True).items():
        setattr(db_task, key, value)
    # Commit the changes to the database
    db.commit()
    # Refresh the user object to reflect the changes in the database
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int):
    task = get_task(db, task_id)
    if not task:
        return None
    db.delete(task)
    db.commit()
    return task


def delete_all_tasks(db: Session, user_id: int):
    tasks = get_all_tasks(db, user_id)
    for task in tasks:
        db.delete(task)
    db.commit()
    return tasks
