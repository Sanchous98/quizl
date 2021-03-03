from dependencies import database
from api.middlewares import is_admin
from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse
from db.repositories import Question as QuestionRepository
from exceptions import BadRequestException, ExceptionScheme
from db.schemas import Question, QuestionCreate, QuestionUpdate

router = APIRouter()
repo = QuestionRepository(next(database()))


@router.post(
    "/",
    dependencies=[Depends(is_admin)],
    responses={200: {"model": Question}, 401: {"model": ExceptionScheme}}
)
def create(question: QuestionCreate) -> Question:
    return repo.create(question)


@router.get("/{question_id}", responses={200: {"model": Question}, 400: {"model": ExceptionScheme}})
def retrieve(question_id: int) -> Question:
    db_question = repo[question_id]

    if db_question is None:
        raise BadRequestException("Question not found")

    return db_question


@router.get(
    "/",
    dependencies=[Depends(is_admin)],
    responses={200: {"model": list[Question]}, 401: {"model": ExceptionScheme}}
)
def retrieve_all() -> list[Question]:
    return repo.all()


@router.put(
    "/{question_id}",
    dependencies=[Depends(is_admin)],
    responses={200: {"model": Question}, 401: {"model": ExceptionScheme}}
)
def update(question_id: int, question: QuestionUpdate) -> Question:
    db_question = repo[question_id]
    db_question.fill(question)

    return db_question


@router.delete("/{question_id}", dependencies=[Depends(is_admin)], responses={401: {"model": ExceptionScheme}})
def delete(question_id: int):
    repo.drop(question_id)

    return JSONResponse()
