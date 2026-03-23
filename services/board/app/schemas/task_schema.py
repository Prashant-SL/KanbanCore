from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class CreateTaskSchema(BaseModel):
    title: str
    description: Optional[str] = None
    board_id: UUID
    column_id: UUID
    position: int
    assigned_to: Optional[str] = None
    
class MoveTaskSchema(BaseModel):
    column_id: UUID
    position: int
    
from datetime import datetime

class TaskResponseSchema(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    board_id: UUID
    column_id: UUID
    position: int
    created_by: str
    assigned_to: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True