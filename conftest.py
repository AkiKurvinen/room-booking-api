import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app

from app.db.database import Base, get_db
from init_database import init_db

# Test database URL - use a separate test database
TEST_DATABASE_URL = "sqlite:///./test_room_booking.db"  # For SQLite
# TEST_DATABASE_URL = "postgresql://user:password@localhost/test_db"  # For PostgreSQL


# Create test engine and sessionmaker at module level
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in TEST_DATABASE_URL else {},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session")
def db_engine():
    """Create test database engine for the entire test session"""
    # Create all tables once for the session
    Base.metadata.create_all(bind=test_engine)
    yield test_engine
    # Optionally drop tables after all tests (uncomment if needed)
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="session")
def db_session(db_engine):
    """Create a single database session for the entire test session"""
    session = TestingSessionLocal()
    # Initialize database with test data once
    init_db(session)
    yield session
    session.close()


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with overridden database dependency"""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass  # Session cleanup is handled by db_session fixture

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


# Optionally, you can keep a clean_db fixture for tests that need a clean database, but it should be session-scoped as well if you want persistence.
