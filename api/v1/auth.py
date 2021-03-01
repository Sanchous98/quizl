from os import getenv
from base64 import b64decode
from datetime import timedelta
from dependencies import database
from fastapi import APIRouter, Depends
from api.middlewares import basic_auth
from exceptions import UnauthorizedException
from fastapi.encoders import jsonable_encoder
from starlette.responses import RedirectResponse
from db.repositories import User as UserRepository
from fastapi.security import OAuth2PasswordRequestForm
from api.security import BasicAuth, Token, create_access_token

router = APIRouter()
repo = UserRepository(next(database()))


@router.post("/token")
def receive_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    user = repo.login(form_data.username, form_data.password)

    if user is None:
        raise UnauthorizedException(detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=int(getenv("ACCESS_TOKEN_EXPIRE", 60)))
    access_token = create_access_token({"sub": user.username}, access_token_expires)

    return Token(access_token=access_token, token_type="bearer")


@router.get("/logout")
async def logout() -> RedirectResponse:
    response = RedirectResponse(url="/docs")
    response.delete_cookie("Authorization", domain="localhost")

    return response


@router.get("/login")
def basic_auth(auth: BasicAuth = Depends(basic_auth)) -> RedirectResponse:
    headers: dict = {"WWW-Authenticate": "Basic"}

    if not auth:
        raise UnauthorizedException(detail="Unauthorized", headers=headers)

    username, _, password = b64decode(auth).decode("ascii").partition(":")

    if repo.login(username, password) is None:
        raise UnauthorizedException(detail="Invalid username or password", headers=headers)

    access_token_expires = timedelta(minutes=int(getenv("ACCESS_TOKEN_EXPIRE", 60)))
    access_token = create_access_token({"sub": username}, access_token_expires)

    response = RedirectResponse(url="/docs")
    response.set_cookie(
        "Authorization",
        value=f"Bearer {jsonable_encoder(access_token)}",
        domain="localhost",
        httponly=True,
        max_age=1800,
        expires=1800
    )

    return response

