from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data.models import create_tables, User, EngWord, RusWord

engine = create_engine('sqlite:///data//sqlite3.db')
engine.connect()


create_tables(engine)


Session = sessionmaker(bind=engine)
session = Session()

session.close()


def add_user(cid, f_name, l_name, username):
    user = User(
        user_tg_id=cid,
        first_name=f_name,
        last_name=l_name,
        username=username
    )
    session.add(user)
    session.commit()


def get_all_users():
    users = session.query(User).all()
    user_ids = [user.user_tg_id for user in users]
    return user_ids


if __name__ == '__main__':
    print(engine)
    get_all_users()

