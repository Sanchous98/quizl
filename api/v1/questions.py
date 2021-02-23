from typing import List
from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse
from db.repositories import Question as QuestionRepository
from db.schemas import Question, QuestionCreate, QuestionUpdate
from dependencies import database

router = APIRouter()
repo = QuestionRepository(next(database()))


@router.post("/")
def create(question: QuestionCreate) -> Question:
    return repo.create(question)


@router.get("/{question_id}")
def retrieve(question_id: int) -> Question:
    db_question = repo.get(question_id)

    if db_question is None:
        raise HTTPException(400, "Question not found")

    return db_question


@router.get("/")
def retrieve_all() -> List[Question]:
    return repo.all()


@router.put("/{question_id}")
def update(question_id: int, question: QuestionUpdate) -> Question:
    db_question = repo.get(question_id)
    db_question.fill(question)

    return db_question


@router.delete("/{question_id}")
def delete(question_id: int):
    repo.drop(question_id)

    return JSONResponse()
