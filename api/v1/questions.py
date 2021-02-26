from typing import List
from dependencies import database
from api.middlewares import is_admin
from fastapi import APIRouter, Depends
from exceptions import BadRequestException
from starlette.responses import JSONResponse
from db.repositories import Question as QuestionRepository
from db.schemas import Question, QuestionCreate, QuestionUpdate

router = APIRouter()
repo = QuestionRepository(next(database()))


@router.post("/", dependencies=[Depends(is_admin)])
def create(question: QuestionCreate) -> Question:
    return repo.create(question)


@router.get("/{question_id}")
def retrieve(question_id: int) -> Question:
    db_question = repo.get(question_id)

    if db_question is None:
        raise BadRequestException("Question not found")

    return db_question


@router.get("/", dependencies=[Depends(is_admin)])
def retrieve_all() -> List[Question]:
    return repo.all()


@router.put("/{question_id}", dependencies=[Depends(is_admin)])
def update(question_id: int, question: QuestionUpdate) -> Question:
    db_question = repo.get(question_id)
    db_question.fill(question)

    return db_question


@router.delete("/{question_id}", dependencies=[Depends(is_admin)])
def delete(question_id: int):
    repo.drop(question_id)

    return JSONResponse()
