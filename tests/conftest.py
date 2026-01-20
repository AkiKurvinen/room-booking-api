import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.session import Base, get_engine
from app.main import app
from fastapi.testclient import TestClient

# Use an in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def test_db():
    engine = get_engine(TEST_DATABASE_URL)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)  # Create tables
    yield TestingSessionLocal()  # Provide the session to the test
    Base.metadata.drop_all(bind=engine)  # Drop tables after the test

@pytest.fixture(scope="function")
def client(test_db):
    # Override the database dependency in the app
    def override_get_db():
        try:
            db = test_db
            yield db
        finally:
            db.close()

    app.dependency_overrides[override_get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides = {}