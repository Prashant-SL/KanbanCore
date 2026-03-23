from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db import Base


class ColumnModel(Base):
    __tablename__ = "columns"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    board_id = Column(
        UUID(as_uuid=True),
        nullable=False
    )

    title = Column(
        String,
        nullable=False
    )

    position = Column(
        Integer
    )