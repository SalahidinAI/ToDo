from passlib.hash import bcrypt
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Enum, ForeignKey, Text, DateTime
from .database import Base
from typing import List, Optional
from enum import Enum as PyEnum
from datetime import datetime


class StatusChoices(str, PyEnum):
    to_do = 'to_do'
    in_progress = 'in_progress'
    completed = 'completed'
    failed = 'failed'


class UserProfile(Base):
    __tablename__ = 'user_profile'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(32))
    last_name: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    username: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String(64), unique=True)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    tasks: Mapped[List['Task']] = relationship('Task', back_populates='user',
                                               cascade='all, delete-orphan')

    def set_password(self, password: str):
        self.password = bcrypt.hash(password)

    def check_password(self, password: str):
        return bcrypt.verify(password, self.password)


class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String, nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    user: Mapped['UserProfile'] = relationship('UserProfile')


class Task(Base):
    __tablename__ = 'task'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(32), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    deadline: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[str] = mapped_column(Enum(StatusChoices), default=StatusChoices.to_do.value)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey('user_profile.id'), nullable=True)

    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='tasks')
