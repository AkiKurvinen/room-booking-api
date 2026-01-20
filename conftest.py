import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import Base, engine
from app.db.session import get_db

# Path to the test database
TEST_DB = "test_room_booking.db"

@pytest.fixture(scope="session", autouse=True)
def drop_database():
    # Ensure the database file is removed before starting tests
    if os.path.exists(TEST_DB):
        try:
            os.remove(TEST_DB)
        except PermissionError:
            print("Could not delete the test database file. Ensure no process is locking it.")

@pytest.fixture(scope="session")
def test_db():
    # Create a test database engine
    from sqlalchemy import create_engine
    test_engine = create_engine(f"sqlite:///{TEST_DB}")

    # Create tables in the test database
    Base.metadata.create_all(bind=test_engine)
    yield TEST_DB

    # Dispose of the engine to close all connections
    test_engine.dispose()

    # Drop tables and remove the test database file
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

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