from abc import ABC
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


class UpdateBase(ABC, BaseModel):
    class Config:
        orm_mode = True


class AnswerBase(BaseModel):
    text: str


class AnswerCreate(AnswerBase):
    correct: bool


class Answer(AnswerBase, UpdateBase):
    id: int
    correct: bool


class AnswerUpdate(Answer, AnswerCreate):
    text: Optional[str]
    correct: Optional[bool]


class QuestionBase(BaseModel):
    text: str


class QuestionCreate(QuestionBase):
    points: int
    answers: List[AnswerCreate]


class Question(QuestionBase, UpdateBase):
    id: int
    answers: List[Answer]


class QuestionUpdate(Question, QuestionCreate):
    text: Optional[str]
    answers: List[AnswerUpdate]
    points: Optional[int]


class GameBase(BaseModel):
    finishes_at: datetime


class GameCreate(GameBase):
    questions: List[QuestionCreate]


class Game(GameBase, UpdateBase):
    id: int
    questions: List[Question]


class GameUpdate(Game, GameCreate):
    finishes_at: Optional[datetime]
    questions: List[QuestionUpdate]


class UserBase(BaseModel):
    firstname: str
    lastname: str
    email: str


class UserCreate(UserBase):
    username: str
    password: str
    is_active: bool = True
    is_super: bool = False

    class Config:
        orm_mode = True


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


class Rank(User):
    points: int
