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
        all_words = session.query(Word).all()
        eng_words_list = [word.eng for word in all_words]
        rus_words_list = [word.rus for word in all_words]
        words = dict(zip(rus_words_list, eng_words_list))
        session.close()
        return words
    except Exception as e:
        print(f'Не получилось получить слова из базы данных. Ошибка: {e}')
        return None


def get_user(cid):
    user = session.query(User).filter(User.id == cid).first()
    session.close()
    return user.id if user else None


def get_user_words(cid):
    try:
        user_words = (
            session.query(Word.rus, Word.eng)
            .join(UserWord, isouter=True)
            .filter(UserWord.user_id.in_([cid, None]))
            .order_by(func.random())
            .limit(4)
            .all()
        )
    except Exception as e:
        print(e)
        session.close()
        return None
    dict_words = {}
    for word_ in user_words:
        dict_words[word_[0]] = word_[1]
    return dict_words


def get_random_eng_word():
    words = session.query(Word).order_by(func.random()).limit(3)
    eng_words = [word.eng for word in words]
    session.close()
    return eng_words


def delete_user_word(cid, eng_word):
    user_id = session.query(User).filter(User.id == cid).first().id
    word_id = session.query(Word).filter(Word.eng == eng_word).first().id
    session.query(UserWord).\
        filter(UserWord.word_id == word_id).\
        filter(UserWord.user_id == user_id).\
        delete()
    session.commit()

    return user_id, word_id


def add_user_word(cid, eng_word):
    user = session.query(User).filter(User.id == cid).first()
    word_id = session.query(Word).filter(Word.eng == eng_word).first().id
    user.words.append(UserWord(user_id=user.id, word_id=word_id))
    session.commit()


def add_new_word(rus_word, eng_word):
    new_word = Word(rus=rus_word, eng=eng_word)
    session.add(new_word)
    session.commit()


def add_default_words():
    w1 = Word(rus='через', eng='through')
    w2 = Word(rus='слишком', eng='too')
    w3 = Word(rus='великий', eng='great')
    w4 = Word(rus='после', eng='after')
    w5 = Word(rus='длинный', eng='long')
    w6 = Word(rus='слышать', eng='hear')
    w7 = Word(rus='поворачивать', eng='turn')
    w8 = Word(rus='чувствовать', eng='feel')
    w9 = Word(rus='голова', eng='head')
    w10 = Word(rus='люди', eng='people')
    session.add_all([w1, w2, w3, w4, w5, w6, w7, w8, w9, w10])
    session.commit()


if __name__ == '__main__':
    print(engine)
    create_tables(engine)
    print(get_user_words(226351277))
    # add_default_words()
    # add_new_word('бежать', 'run')
    # add_user_word(226351277, 'run')
    # print(get_all_words())
    # print(dir(delete_user_word(226351277)))
    # print(delete_user_word(226351277))
    # print(get_user_words(226351277))
    # add_rus_words()
