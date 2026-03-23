from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import EmailStr

from app.db import get_db
from app.models.tasks_model import Tasks
from app.schemas.task_schema import CreateTaskSchema, MoveTaskSchema, TaskResponseSchema
from app.utils.dependencies import get_current_user

from fastapi import Request

router = APIRouter()

@router.post("/tasks")
def create_tasks(
    data: CreateTaskSchema,
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = Tasks(
        board_id=data.board_id,
        column_id=data.column_id,
        title=data.title,
        description=data.description,
        position=data.position,
        created_by=user,
        assigned_to=data.assigned_to
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task

@router.get("/tasks")
def get_tasks(
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    tasks = db.query(Tasks).filter(Board.owner_id == user).all()
    return tasks
