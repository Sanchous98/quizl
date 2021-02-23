from typing import List
from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse
from db.repositories import Game as GameRepository
from db.schemas import Game, GameCreate, GameUpdate
from dependencies import database

router = APIRouter()
repo = GameRepository(next(database()))


@router.post("/")
def create(game: GameCreate) -> Game:
    return repo.create(game)


@router.get("/{game_id}")
def retrieve(game_id: int) -> Game:
    db_game = repo.get(game_id)

    if db_game is None:
        raise HTTPException(400, "Game not found")

    return db_game


@router.get("/")
def retrieve_all() -> List[Game]:
    return repo.all()


@router.put("/{game_id}")
def update(game_id: int, game: GameUpdate) -> Game:
    db_game = repo.get(game_id)
    db_game.fill(game)

    return db_game


@router.delete("/{game_id}")
def delete(game_id: int):
    repo.drop(game_id)

    return JSONResponse()
