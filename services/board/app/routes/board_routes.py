from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import EmailStr

from app.db import get_db
from app.models.board_model import Board
from app.schemas.board_schema import CreateBoardSchema
from app.utils.dependencies import get_current_user

from fastapi import Request

router = APIRouter()

@router.post("/boards")
def create_board(
    data: CreateBoardSchema,
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    board = Board(
        title=data.title,
        owner_id=user
    )

    db.add(board)
    db.commit()
    db.refresh(board)

    return board

@router.get("/boards")
def get_boards(
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    boards = db.query(Board).filter(Board.owner_id == user).all()
    return boards
