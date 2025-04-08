from pydantic import BaseModel, EmailStr, validator
from .models import StatusChoices
from typing import Optional
from datetime import datetime, timezone


class UserProfileSchema(BaseModel):
    first_name: str
    last_name: Optional[str]
    username: str
    password: str
    email: EmailStr
    age: Optional[int]

    class Config:
        from_attributes = True


class TaskCreateSchema(BaseModel):
    title: str
    description: str
    deadline: datetime

    class Config:
        from_attributes = True


class TaskUpdateSchema(BaseModel):
    status: StatusChoices

    class Config:
        from_attributes = True


class TaskSchema(BaseModel):
    title: str
    description: str
    deadline: datetime
    status: StatusChoices
    user_id: int

    @validator("deadline")
    def deadline_cannot_be_in_future(cls, value: datetime):
        if value > datetime.utcnow():
            raise ValueError("Deadline cannot be in the future.")
        return value

    class Config:
        from_attributes = True
