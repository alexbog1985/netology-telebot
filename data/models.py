import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    pass


class EngWord(Base):
    pass


class RusWord(Base):
    pass
