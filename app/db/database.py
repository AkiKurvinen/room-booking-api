import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

TESTING = os.getenv("TESTING", "False").lower() == "true"
if TESTING:
    SQLALCHEMY_DATABASE_URL = os.getenv(
        "TEST_DATABASE_URL", "sqlite:///./test_room_booking.db"
    )
else:
    SQLALCHEMY_DATABASE_URL = os.getenv(
        "SQLALCHEMY_DATABASE_URL", "sqlite:///./room_booking.db"
    )


def get_engine(database_url=SQLALCHEMY_DATABASE_URL):
    connect_args = {"check_same_thread": False} if "sqlite" in database_url else {}
    return create_engine(database_url, connect_args=connect_args)


engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
