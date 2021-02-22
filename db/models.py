from typing import Type
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from .schemas import UserBase, GameBase, QuestionBase, AnswerBase


class Fillable:
    id = Column("id", Integer, primary_key=True)

    @property
    def schema(self) -> Type[BaseModel]:
        return BaseModel

    def fill(self, schema: schema):
        for key, value in schema.dict().items():
            if value is not None:
                self.__setattr__(key, value)


class User(Fillable, Base):
    __tablename__ = "users"

    firstname = Column("firstname", String(255), nullable=False)
    lastname = Column("lastname", String(255), nullable=False)
    email = Column("email", String(255), nullable=False)
    password = Column("password", String(255), nullable=False)
    is_active = Column("is_active", Boolean, default=True, nullable=False)
    is_super = Column("is_super", Boolean, default=False, nullable=False)
    games = relationship("Game", back_populates="player")

    @property
    def schema(self) -> Type[UserBase]:
        return UserBase


class Game(Fillable, Base):
    __tablename__ = "games"

    player_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    player = relationship("User", back_populates="games")

    @property
    def schema(self) -> Type[GameBase]:
        return GameBase


class Question(Fillable, Base):
    __tablename__ = "questions"

    text = Column("text", Text, nullable=False)
    answers = relationship("Answer", back_populates="question")
    correct_answer = relationship("Answer")

    @property
    def schema(self) -> Type[QuestionBase]:
        return QuestionBase


class Answer(Fillable, Base):
    __tablename__ = "answers"

    text = Column("text", Text, nullable=False)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)
    question = relationship("Question", back_populates="answers")

    @property
    def schema(self) -> Type[AnswerBase]:
        return AnswerBase
