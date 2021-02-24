from typing import Union
from db.database import SessionLocal
from passlib.context import CryptContext


def database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hash_password(password: Union[str, bytes]) -> str:
    return CryptContext(schemes=["bcrypt"], deprecated="auto").hash(password)
