from fastapi import Depends
import os
from sqlmodel import create_engine, SQLModel, Session

sqlite_file_name = "../../database.sqlite"
base_dir = os.path.dirname(os.path.realpath(__file__))
database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}"

engine = create_engine(database_url, echo=True)

def init_db():
	SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
