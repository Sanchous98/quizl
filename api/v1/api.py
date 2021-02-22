from fastapi import APIRouter
from . import users, questions, answers, games

router = APIRouter()
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(questions.router, prefix="/questions", tags=["questions"])
router.include_router(games.router, prefix="/games", tags=["games"])
router.include_router(answers.router, prefix="/answers", tags=["answers"])
