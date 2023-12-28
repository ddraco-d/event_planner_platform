from __future__ import annotations

from pydantic import BaseModel
from datetime import datetime, date


class UserLogin(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    id: int
    role: str


class UserCreate(BaseModel):
    username: str
    password: str


class User(BaseModel):
    id: int
    username: str
    is_active: bool
    role: str

    class Config:
        orm_mode = True


class EventBase(BaseModel):
    title: str
    description: str


class EventCreate(EventBase):
    date: date


class Event(EventBase):
    id: int
    date: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    exp: int


class TokenData(BaseModel):
    username: str = None


class Comment(BaseModel):
    id: int
    comment: str
    event_id: int
    user_id: int


class CommentCreate(BaseModel):
    comment: str


class Ticket(BaseModel):
    id: int
    user_id: int
    event_id: int


class HasTicket(BaseModel):
    has_ticket: bool
