from __future__ import annotations
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True)
    firstname = Column("firstname", String(255))
    lastname = Column("lastname", String(255))
    email = Column("email", String(255))
    password = Column("password", String(255))
    is_active = Column("is_active", Boolean)
    is_super = Column("is_super", Boolean)
    games = relationship("Game", back_populates="player")


class Game(Base):
    __tablename__ = "games"

    id = Column("id", Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('users.id'))
    player = relationship("User", back_populates="games")


class Question(Base):
    __tablename__ = "questions"

    id = Column("id", Integer, primary_key=True)
    text = Column("text", Text)
    answers = relationship("Answer", back_populates="answers")
    correct_answer = relationship("Answer")


class Answer(Base):
    __tablename__ = "answers"

    id = Column("id", Integer, primary_key=True)
    text = Column("text", Text)
    question_id = Column(Integer, ForeignKey('questions.id'))
    question = relationship("Question", back_populates="answers")
