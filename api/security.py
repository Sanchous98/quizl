import os
from datetime import datetime, timedelta
from typing import Optional, Union
from jwt import encode, decode
from fastapi import Depends, HTTPException
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel, OAuthFlowPassword
from fastapi.security import OAuth2
from fastapi.security.base import SecurityBase
from fastapi.security.utils import get_authorization_scheme_param
from passlib.context import CryptContext
from pydantic import BaseModel
from starlette.requests import Request
from db import models
from db.repositories import User
from dependencies import database


class BasicAuth(SecurityBase):
    def __init__(self, scheme_name: str = __class__.__name__, auto_error: bool = True):
        self.scheme_name = scheme_name
        self.auto_error = auto_error

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)

        if not authorization or scheme.lower() != "basic":
            if self.auto_error:
                raise HTTPException(status_code=401, detail="Unauthorized")
            else:
                return None

        return param


class OAuth2PasswordBearerCookie(OAuth2):
    def __init__(self, token_url: str, scheme_name: str = None, scopes: dict = None, auto_error: bool = True):
        if scopes is None:
            scopes = {}

        flows = OAuthFlowsModel(password=OAuthFlowPassword(tokenUrl=token_url, scopes=scopes))
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        header_authorization: str = request.headers.get("Authorization")
        cookie_authorization: str = request.cookies.get("Authorization")
        header_scheme, header_param = get_authorization_scheme_param(header_authorization)
        cookie_scheme, cookie_param = get_authorization_scheme_param(cookie_authorization)

        if header_scheme.lower() == "bearer":
            authorization = True
            scheme = header_scheme
            param = header_param
        elif cookie_scheme.lower() == "bearer":
            authorization = True
            scheme = cookie_scheme
            param = cookie_param
        else:
            authorization = False
            scheme = param = ""

        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(status_code=401, detail="Unauthorized")
            else:
                return None

        return param


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None


oauth2_scheme = OAuth2PasswordBearerCookie(token_url="/token")
basic_auth = BasicAuth(auto_error=False)
repo = User(next(database()))


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    return encode(data.copy().update({"exp": datetime.utcnow() + expires_delta}), os.getenv("SECRET_KEY"), algorithm="HS256")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")
    payload = decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
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
        raise HTTPException(status_code=401, detail="Inactive user")

    return current_user


def hash_password(password: Union[str, bytes]) -> str:
    return CryptContext(schemes=["bcrypt"], deprecated="auto").hash(password)
