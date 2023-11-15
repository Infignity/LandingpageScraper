'''defining database connection'''
import os
from typing import Any
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from src.db
from src.app_config import (
    DB_USER,
    DB_PASS,
    DB_NAME
)


SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{passwd}@localhost:5432/{db_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base: Any = declarative_base()

def connect_db():
    """connect db"""
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        