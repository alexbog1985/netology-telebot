from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from data.models import create_tables, User, EngWord, RusWord

engine = create_engine('sqlite:///data//sqlite3.db')
engine.connect()


create_tables(engine)


Session = sessionmaker(bind=engine)
session = Session()

session.close()


def add_user(cid, user_chat_id, f_name, l_name, username, step):
    user = User(
        user_tg_id=cid,
        user_chat_id=user_chat_id,
        first_name=f_name,
        last_name=l_name,
        username=username,
        step=step
    )
    session.add(user)
    session.commit()


def get_all_users():
    users = session.query(User).all()
    user_ids = [user.user_tg_id for user in users]
    return user_ids


def get_user_words(cid):
    user = session.query(User).filter(cid)
    word = user.eng_words.first()
    print(word)


def get_rus_words():
    q = (session.query(
        RusWord,
        EngWord
    ).select_from(RusWord).
       join(EngWord).
       group_by(func.random()).
       group_by(EngWord.eng_word).
       first())

    print(q[0].rus_word, q[1].eng_word)
    # for w, e in q:
    #     print(w.rus_word, e.eng_word)

def add_rus_words():
    w1 = RusWord(rus_word='через')
    w2 = RusWord(rus_word='слишком')
    w3 = RusWord(rus_word='великий')
    w4 = RusWord(rus_word='после')
    w5 = RusWord(rus_word='длинный')
    w6 = RusWord(rus_word='слышать')
    w7 = RusWord(rus_word='поворачивать')
    w8 = RusWord(rus_word='чувствовать')
    w9 = RusWord(rus_word='слишком')
    w10 = RusWord(rus_word='люди')
    session.add_all([w1, w2, w3, w4, w5, w6, w7, w8, w9, w10])
    session.commit()


def add_eng_words():
    w1 = EngWord(eng_word='through', rus_word_id=1)
    w2 = EngWord(eng_word='too', rus_word_id=2)
    w3 = EngWord(eng_word='great', rus_word_id=3)
    w4 = EngWord(eng_word='after', rus_word_id=4)
    w5 = EngWord(eng_word='long', rus_word_id=5)
    w6 = EngWord(eng_word='hear', rus_word_id=6)
    w7 = EngWord(eng_word='turn', rus_word_id=7)
    w8 = EngWord(eng_word='feel', rus_word_id=8)
    w9 = EngWord(eng_word='head', rus_word_id=9)
    w10 = EngWord(eng_word='people', rus_word_id=10)
    session.add_all([w1, w2, w3, w4, w5, w6, w7, w8, w9, w10])
    session.commit()

if __name__ == '__main__':
    print(engine)
    get_all_users()
    get_rus_words()
    # add_rus_words()
    # add_eng_words()
