from pydantic import BaseModel
from uuid import UUID


class ColumnBase(BaseModel):
    title: str
    
class CreateColumnSchema(ColumnBase):
    position: int
    
class ColumnResponseSchema(ColumnBase):
    id: UUID
    board_id: UUID
    position: int

    class Config:
        from_attributes = True