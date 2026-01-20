import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Default database URL
SQLALCHEMY_DATABASE_URL = os.getenv(
    "SQLALCHEMY_DATABASE_URL", "sqlite:///./room_booking.db"
)


# Allow overriding the database URL for testing
def get_engine(database_url=SQLALCHEMY_DATABASE_URL):
    connect_args = {"check_same_thread": False} if "sqlite" in database_url else {}
    return create_engine(database_url, connect_args=connect_args)


engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
