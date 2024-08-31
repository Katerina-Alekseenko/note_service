from pydantic import BaseModel


class Note(BaseModel):
    id: int
    user_id: int
    content: str
