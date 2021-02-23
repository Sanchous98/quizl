from typing import List
from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse
from db.repositories import Answer as AnswerRepository
from db.schemas import Answer, AnswerCreate, AnswerUpdate
from dependencies import database

router = APIRouter()
repo = AnswerRepository(next(database()))


@router.post("/")
def create(answer: AnswerCreate) -> Answer:
    return repo.create(answer)


@router.get("/{answer_id}")
def retrieve(answer_id: int) -> Answer:
    db_answer = repo.get(answer_id)

    if db_answer is None:
        raise HTTPException(400, "Question not found")

    return db_answer


@router.get("/")
def retrieve_all() -> List[Answer]:
    return repo.all()


@router.put("/{answer_id}")
def update(answer_id: int, answer: AnswerUpdate) -> Answer:
    db_answer = repo.get(answer_id)
    db_answer.fill(answer)

    return db_answer


@router.delete("/{answer_id}")
def delete(answer_id: int):
    repo.drop(answer_id)

    return JSONResponse()
