from db import models
from os import getenv
from jwt import decode
from fastapi import Depends
from db.repositories import User
from dependencies import database
from exceptions import ForbiddenException, UnauthorizedException
from api.security import OAuth2PasswordBearerCookie, BasicAuth, TokenData

oauth2_scheme = OAuth2PasswordBearerCookie(token_url="/token")
basic_auth = BasicAuth(auto_error=False)
repo = User(next(database()))


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = UnauthorizedException(detail="Could not validate credentials")
    payload = decode(token, getenv("SECRET_KEY"), algorithms=["HS256"])
    username: str = payload.get("sub")

    if username is None:
        raise credentials_exception

    token_data = TokenData(username=username)
    user = repo.get_by_username(token_data.username)

    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise UnauthorizedException(detail="Inactive user")

    return current_user


async def is_admin(user: models.User = Depends(get_current_active_user)):
    if not user.is_super:
        raise ForbiddenException()
