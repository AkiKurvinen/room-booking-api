import pytest
from app.main import app

def test_app_running():
    # Example test to check if the app is running
    assert app is not None