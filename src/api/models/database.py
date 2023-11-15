"""lib import"""
from .db import SessionLocal


def connect_db():
    """connect db"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        