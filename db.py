import random
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from data.models import create_tables, User, Word, UserWord

engine = create_engine('sqlite:///data//sqlite3.db')
engine.connect()


create_tables(engine)


Session = sessionmaker(bind=engine)
session = Session()

session.close()


def add_user(cid, f_name, l_name, username, step):
    user = User(
        id=cid,
        first_name=f_name,
        last_name=l_name,
        username=username,
        step=step
    )
    default_words = session.query(Word).limit(10).all()
    for word_ in default_words:
        user.words.append(UserWord(user_id=user.id, word_id=word_.id))

    session.add(user)
    session.commit()


def get_all_users():
    users = session.query(User).all()
    user_ids = [user.id for user in users]
    session.close()
    return user_ids


def get_all_words():
    try:
        e_words = session.query(EngWord).all()
        r_words = session.query(RusWord).all()
        eng_words_list = [word.eng_word for word in e_words]
        rus_words_list = [word.rus_word for word in r_words]
        words = dict(zip(rus_words_list, eng_words_list))
        session.close()
        return words
    except Exception as e:
        print(f'Не получилось получить слова из базы данных. Ошибка: {e}')
        return None


def get_user(cid):
    user = session.query(User).filter(User.user_tg_id == cid).first()
    session.close()
    return user.user_tg_id if user else None


def get_user_words(cid):
    try:
        user = session.query(User).filter(User.user_tg_id == cid).first()
        words = [word.eng_words.eng_word for word in user.eng_words]
        russian_words = [word.eng_words.rus_word.rus_word for word in user.eng_words]
        eng_rus_words = list(zip(russian_words, words))

        two_word = random.choice(eng_rus_words)
        session.close()
    except Exception as e:
        print(e)
        session.close()
        return None
    return {'rus_word': two_word[0], 'eng_word': two_word[1]}


def get_random_eng_word():
    q = (session.query(
        EngWord
    ).select_from(EngWord).
       group_by(func.random()).
       first())
    session.close()
    return q.eng_word


def delete_user_word(cid, eng_word):
    user_id = session.query(User).filter(User.user_tg_id == cid).first().id
    word_id = session.query(EngWord).filter(EngWord.eng_word == eng_word).first().id
    session.query(UserToEngWord).\
        filter(UserToEngWord.eng_word_id == word_id).\
        filter(UserToEngWord.user_id == user_id).\
        delete()
    session.commit()

    return user_id, word_id


def add_user_word(cid, eng_word):
    user = session.query(User).filter(User.user_tg_id == cid).first()
    word_id = session.query(EngWord).filter(EngWord.eng_word == eng_word).first().id
    user.eng_words.append(UserToEngWord(user_id=user.id, eng_word_id=word_id))
    session.commit()


def add_new_word(r_word, eng_word):
    rus_word = RusWord(rus_word=r_word)
    session.add(rus_word)
    session.commit()
    rus_word_id = session.query(RusWord).filter(RusWord.rus_word == r_word).first().id
    e_word = EngWord(eng_word=eng_word, rus_word_id=rus_word_id)
    session.add(e_word)
    session.commit()


def add_default_words():
    w1 = Word(rus='через', eng='through'),
    w2 = Word(rus='слишком', eng='too'),
    w3 = Word(rus='великий', eng='great'),
    w4 = Word(rus='после', eng='after'),
    w5 = Word(rus='длинный', eng='long'),
    w6 = Word(rus='слышать', eng='hear'),
    w7 = Word(rus='поворачивать', eng='turn'),
    w8 = Word(rus='чувствовать', eng='feel'),
    w9 = Word(rus='голова', eng='head'),
    w10 = Word(rus='люди', eng='people'),
    session.add_all([w1, w2, w3, w4, w5, w6, w7, w8, w9, w10])
    session.commit()


if __name__ == '__main__':
    print(engine)
    # create_tables(engine)
    # add_new_word('бежать', 'run')
    # add_user_word(226351277, 'run')
    # print(get_all_words())
    # print(dir(delete_user_word(226351277)))
    # print(delete_user_word(226351277))
    # print(get_user_words(226351277))
    # add_rus_words()
    # add_eng_words()

