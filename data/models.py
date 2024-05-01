from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()


class UserToEngWord(Base):
    __tablename__ = 'user_eng_word'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    eng_word_id = Column(Integer, ForeignKey('eng_word.id'))


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    user_tg_id = Column(Integer, nullable=False, unique=True)
    user_chat_id = Column(Integer, nullable=False, unique=True)
    first_name = Column(String(length=50))
    last_name = Column(String(length=50))
    username = Column(String(length=50))
    step = Column(Integer, default=0)

    eng_words = relationship('UserToEngWord', backref='users')


class EngWord(Base):
    __tablename__ = 'eng_word'

    id = Column(Integer, primary_key=True)
    eng_word = Column(String)
    rus_word_id = Column(Integer, ForeignKey('rus_word.id'))

    rus_word = relationship('RusWord', backref='rus_words')
    users = relationship('UserToEngWord', backref='eng_words')


class RusWord(Base):
    __tablename__ = 'rus_word'

    id = Column(Integer, primary_key=True)
    rus_word = Column(String)


def create_tables(engine):
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
