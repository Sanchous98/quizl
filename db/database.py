from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from inflection import underscore, pluralize
from sqlalchemy.ext.declarative import declarative_base, declared_attr

engine = create_engine(getenv("DATABASE_URL"), connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=True, autoflush=True, bind=engine)


class Base:
    @declared_attr
    def __tablename__(self):
        return pluralize(underscore(self.__class__.__name__))


Base = declarative_base(cls=Base)
