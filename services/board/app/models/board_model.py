from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db import Base

class Board(Base):
    __tablename__ = "boards"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    
    title = Column(
        String, 
        nullable=False
    )
    
    owner_id = Column(
        String,
        nullable=False
    )