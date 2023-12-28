# app/api/routers/tasks.py

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.api.database.db import get_db
from app.api.schemas.task import TaskCreate, Task
from app.api.crud.task import create_task, get_task, update_task, delete_task


router = APIRouter()


@router.get("/tasks")
def get_tasks():
    return {"message": "Get all tasks"}


@router.post("/create-task/", response_model=Task)
def create_new_task(
    task: TaskCreate, db: Session = Depends(get_db), request: Request = None
):
    user_id = int(request.session.get("user_id"))
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="User not authenticated",
        )
    # task["user_id"] = user_id
    print("USER ID", user_id)
    return create_task(db, task, user_id)


@router.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = get_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.put("/tasks/{task_id}", response_model=Task)
def update_existing_task(task_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    db_task = get_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return update_task(db, task_id, task)


@router.delete("/tasks/{task_id}", response_model=Task)
def delete_existing_task(task_id: int, db: Session = Depends(get_db)):
    db_task = get_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    delete_task(db, task_id)
    return db_task
