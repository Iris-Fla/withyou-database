import time
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def wait_for_db():
    print("Connecting to database...")
    retries = 10
    while retries > 0:
        try:
            # 実際に接続を試みる
            connection = engine.connect()
            connection.close()
            print("Database connected!")
            return
        except OperationalError:
            retries -= 1
            print(f"Database not ready, retrying... ({retries} attempts left)")
            time.sleep(3)  # 3秒待機
    raise Exception("Could not connect to the database")
# -----------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()