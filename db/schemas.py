from abc import ABC
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


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
    answers: list[AnswerCreate] = []


class Question(QuestionBase, UpdateBase):
    id: int
    answers: list[Answer] = []


class QuestionUpdate(Question, QuestionCreate):
    text: Optional[str]
    answers: Optional[list[AnswerUpdate]] = []
    points: Optional[int]


class GameBase(BaseModel):
    finishes_at: datetime


class GameCreate(GameBase):
    questions: list[QuestionCreate] = []


class Game(GameBase, UpdateBase):
    id: int
    questions: list[Question] = []


class GameUpdate(Game, GameCreate):
    finishes_at: Optional[datetime]
    questions: list[QuestionUpdate] = []


class UserBase(BaseModel):
    firstname: str
    lastname: str
    email: str


class UserCreate(UserBase):
    username: str
    password: str

    class Config:
        orm_mode = True


class User(UserBase, UpdateBase):
    id: int
    is_active: bool
    games: list[Game] = []


class UserUpdate(UserCreate, UpdateBase):
    firstname: Optional[str]
    lastname: Optional[str]
    email: Optional[str]
    password: Optional[str]
    is_active: Optional[bool]


class Rank(User):
    points: int
