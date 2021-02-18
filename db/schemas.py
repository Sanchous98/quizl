from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel


class QuestionBase(BaseModel):
    pass


class AnswerBase(BaseModel):
    pass


class GameBase(BaseModel):
    pass


class Game(GameBase):
    id: int
    player: User

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserCreate):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    is_active: Optional[bool]


class User(UserBase):
    id: int
    is_active: bool
    games: List[Game] = []

    class Config:
        orm_mode = True
