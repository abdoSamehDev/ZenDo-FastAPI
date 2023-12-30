from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.api.database.db import get_db
from app.api.schemas.task import TaskCreate, Task
from app.api.crud.task import (
    get_all_tasks,
    create_task,
    get_task,
    update_task,
    delete_task,
    delete_all_tasks,
)
from typing import List


router = APIRouter()


@router.get("/", response_model=List[Task])
def get_all_user_tasks(db: Session = Depends(get_db), request: Request = None):
    user_id = request.session.get("user_id")
    print("User ID in get all tasks: ", str(user_id))
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="User not authenticated",
        )
    tasks = get_all_tasks(db, user_id)
    if tasks is None:
        raise HTTPException(status_code=404, detail="Tasks not found")
    return tasks


@router.post("/create-task/", response_model=Task)
def create_new_task(
    task: TaskCreate, db: Session = Depends(get_db), request: Request = None
):
    user_id = request.session.get("user_id")
    print("User ID in create new task: ", str(user_id))
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="User not authenticated",
        )
    print("USER ID", user_id)
    return create_task(db, task, user_id)


@router.get("/{task_id}", response_model=Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = get_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.put("/update/{task_id}", response_model=Task)
def update_existing_task(task_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    updated_task = update_task(db, task_id, task)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@router.delete("/delete/{task_id}")
def delete_existing_task(task_id: int, db: Session = Depends(get_db)):
    deleted_task = delete_task(db, task_id)
    if deleted_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}


@router.delete("/delete-all")
def delete_all_user_tasks(db: Session = Depends(get_db), request: Request = None):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="User not authenticated",
        )
    deleted_task = delete_all_tasks(db, user_id)
    if deleted_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "All tasks deleted successfully"}
