from typing import List
from dependencies import database
from api.middlewares import is_admin
from fastapi import APIRouter, Depends
from exceptions import BadRequestException
from starlette.responses import JSONResponse
from db.repositories import Answer as AnswerRepository
from db.schemas import Answer, AnswerCreate, AnswerUpdate

router = APIRouter()
repo = AnswerRepository(next(database()))


@router.post("/", dependencies=[Depends(is_admin)])
def create(answer: AnswerCreate) -> Answer:
    return repo.create(answer)


@router.get("/{answer_id}")
def retrieve(answer_id: int) -> Answer:
    db_answer = repo.get(answer_id)

    if db_answer is None:
        raise BadRequestException("Question not found")

    return db_answer


@router.get("/", dependencies=[Depends(is_admin)])
def retrieve_all() -> List[Answer]:
    return repo.all()


@router.put("/{answer_id}", dependencies=[Depends(is_admin)])
def update(answer_id: int, answer: AnswerUpdate) -> Answer:
    db_answer = repo.get(answer_id)
    db_answer.fill(answer)

    return db_answer


@router.delete("/{answer_id}", dependencies=[Depends(is_admin)])
def delete(answer_id: int):
    repo.drop(answer_id)

    return JSONResponse()
