from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Todo base model for shared properties
class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

# Todo create model (used for creating a new todo)
class TodoCreate(TodoBase):
    pass

# Todo model (used for responses)
class Todo(TodoBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True
