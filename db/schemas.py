from __future__ import annotations
from abc import ABC
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional, Union


class UpdateBase(ABC, BaseModel):
    class Config:
        orm_mode = True


class QuestionBase(BaseModel):
    text: str
    answers: List[AnswerCreate] = []


class QuestionCreate(QuestionBase):
    points: int
    answers: List[AnswerCreate] = []


class Question(QuestionBase, UpdateBase):
    id: int
    answers: List[Answer] = []


class QuestionUpdate(Question, QuestionCreate):
    text: Optional[str]
    answers: Optional[List[AnswerUpdate, AnswerCreate]] = []
    points: Optional[int]


class AnswerBase(BaseModel):
    text: str


class AnswerCreate(AnswerBase):
    correct: bool


class Answer(AnswerBase, UpdateBase):
    id: int


class AnswerUpdate(Answer, AnswerCreate):
    text: Optional[str]
    correct: Optional[bool]


class GameBase(BaseModel):
    finishes_at: datetime
    questions: List[QuestionCreate] = []


class GameCreate(GameBase):
    questions: List[QuestionCreate] = []


class Game(GameBase, UpdateBase):
    id: int
    questions: List[Question] = []


class GameUpdate(Game, GameCreate):
    finishes_at: Optional[datetime]
    questions: List[Union[QuestionCreate, QuestionUpdate]] = []


class UserBase(BaseModel):
    firstname: str
    lastname: str
    email: str


class UserCreate(UserBase):
    username: str
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
