from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import create_tables, User, EngWord, RusWord

engine = create_engine('sqlite:///sqlite3.db')
engine.connect()


create_tables(engine)


Session = sessionmaker(bind=engine)
session = Session()


session.close()

if __name__ == '__main__':
    print(engine)

