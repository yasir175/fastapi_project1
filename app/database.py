# print("database.py loading...")
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg
from psycopg.rows import dict_row
import time
from pickle import TRUE
from .config import setting

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{setting.database_username}:{setting.database_password}@{setting.database_hostname}:{setting.database_port}/{setting.database_name}"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()

def get_db():
    # print("get_db defined")

    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while TRUE:
#     try:
#         conn = psycopg.connect(
#             host="localhost",
#             dbname="fastapi-project_01",
#             user="postgres",
#             password="4544",
#             port="5432",  
#         )
#         cursor=conn.cursor(row_factory=dict_row)
#         print("database connection was successfull")
#         break
#     except Exception as error:
#         print("connection to database failed")
#         print("error: ", error)
#         time.sleep(2)
