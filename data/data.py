from sqlalchemy import create_engine

engine = create_engine('sqlite:///sqlite3.db')
engine.connect()

if __name__ == '__main__':
    print(engine)

