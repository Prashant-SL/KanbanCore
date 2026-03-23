from pydantic import BaseModel

class CreateBoardSchema(BaseModel):
    title: str