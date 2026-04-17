from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.db import get_db
from app.models.tasks_model import Tasks
from app.models.board_model import Board
from app.schemas.task_schema import CreateTaskSchema, MoveTaskSchema, TaskResponseSchema
from app.utils.dependencies import get_current_user

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
    tasks = db.query(Tasks).join(Board, Tasks.board_id == Board.id).filter(Board.owner_id == user).all()
    return tasks

@router.patch("/tasks/{task_id}/move")
def move_task(
    task_id: UUID,
    data: MoveTaskSchema,
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = db.query(Tasks).filter(Tasks.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.column_id = data.column_id
    task.position = data.position

    db.commit()
    db.refresh(task)

    return task
