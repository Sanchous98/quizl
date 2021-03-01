from fastapi import APIRouter
from . import users, questions, answers, games, auth, rankings

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(rankings.router, prefix="/rankings", tags=["Rankings"])
router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(questions.router, prefix="/questions", tags=["Questions"])
router.include_router(games.router, prefix="/games", tags=["Games"])
router.include_router(answers.router, prefix="/answers", tags=["Answers"])
