import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import Base, engine, SessionLocal, Room, Booking
from app.db.session import get_db
from datetime import datetime

@pytest.fixture(scope="module")
def test_db():
    # Create tables in the test database
    Base.metadata.create_all(bind=engine)

    # Create a new session
    session = SessionLocal()

    try:
        # Add initial data
        room = Room(id=1, name="neukkari")
        booking = Booking(
            id=1, room_id=1, start_time=datetime.now(), end_time=datetime.now()
        )

        session.add(room)
        session.add(booking)
        session.commit()

        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client(test_db):
    # Override the database dependency
    def override_get_db():
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker

        test_engine = create_engine(f"sqlite:///{test_db}")
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client