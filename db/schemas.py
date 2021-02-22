from __future__ import annotations
from abc import ABC
from typing import List, Optional
from pydantic import BaseModel


class UpdateBase(ABC, BaseModel):
    class Config:
        orm_mode = True


class QuestionBase(BaseModel):
    pass


class QuestionCreate(QuestionBase):
    pass


class Question(QuestionBase, UpdateBase):
    id: int


class QuestionUpdate(Question, QuestionCreate):
    pass


class AnswerBase(BaseModel):
    pass


class AnswerCreate(AnswerBase):
    pass


class Answer(AnswerBase, UpdateBase):
    pass


class AnswerUpdate(Answer, AnswerCreate):
    pass


class GameBase(BaseModel):
    pass


class GameCreate(GameBase):
    pass


class Game(GameBase, UpdateBase):
    player: User


class GameUpdate(Game, GameCreate):
    pass


class UserBase(BaseModel):
    firstname: str
    lastname: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase, UpdateBase):
    id: int
    is_active: bool
    games: List[Game] = []


class UserUpdate(UserCreate, UpdateBase):
    firstname: Optional[str]
    lastname: Optional[str]
    email: Optional[str]
    password: Optional[str]
    is_active: Optional[bool]
