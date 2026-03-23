from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.db import get_db
from app.models.column_model import ColumnModel
from app.models.board_model import Board
from app.schemas.column_schema import CreateColumnSchema
from app.utils.dependencies import get_current_user

router = APIRouter()

@router.post("/boards/{board_id}/columns")
def create_column(
    board_id: UUID,
    data: CreateColumnSchema,
    user_id=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    board = db.query(Board).filter(
        Board.id == board_id,
        Board.owner_id == user_id
    ).first()

    if not board:
        raise HTTPException(status_code=404, detail="Board not found")

    column = ColumnModel(
        title=data.title,
        board_id=board_id,
        position=data.position
    )

    db.add(column)
    db.commit()
    db.refresh(column)

    return column

@router.get("/boards/{board_id}/columns")
def get_columns(
    board_id: UUID,
    user_id=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    board = db.query(Board).filter(
        Board.id == board_id,
        Board.owner_id == user_id
    ).first()

    if not board:
        raise HTTPException(status_code=404, detail="Board not found")

    columns = db.query(ColumnModel).filter(
        ColumnModel.board_id == board_id
    ).order_by(ColumnModel.position).all()

    return columns