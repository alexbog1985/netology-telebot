from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()


class UserWord(Base):
    __tablename__ = 'user_word'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    word_id = Column(Integer, ForeignKey('word.id'))


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=False)
    first_name = Column(String(length=50))
    last_name = Column(String(length=50))
    username = Column(String(length=50))
    step = Column(Integer, default=0)

    words = relationship('UserWord', backref='users')


class Word(Base):
    __tablename__ = 'word'

    id = Column(Integer, primary_key=True)
    eng = Column(String(length=50))
    rus = Column(String(length=50))

    users = relationship('UserWord', backref='words')


def create_tables(engine):
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
