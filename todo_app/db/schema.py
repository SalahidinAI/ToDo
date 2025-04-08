from pydantic import BaseModel, EmailStr
from .models import StatusChoices
from typing import Optional
from datetime import datetime


class UserProfileSchema(BaseModel):
    first_name: str
    last_name: Optional[str]
    username: str
    password: str
    email: EmailStr
    age: Optional[int]

    class Config:
        from_attributes = True


class TaskSchema(BaseModel):
    title: str
    description: str
    deadline: datetime
    status: StatusChoices
    user_id: int

    class Config:
        from_attributes = True
