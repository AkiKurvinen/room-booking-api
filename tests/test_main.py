import os
import pytest
from app.main import app
from fastapi.testclient import TestClient

API_URL = os.getenv("API_URL", "/api/v1")

def test_app_running():
    # Example test to check if the app is running
    assert app is not None

client = TestClient(app)

def test_read_root():
    response = client.get(f"{API_URL}/")
    assert response.status_code == 200
    assert response.json() == {"message": "Room Booking API is running"}

def test_create_and_get_booking(client):
    # Create a new booking
    response = client.post(
        f"{API_URL}/bookings/",
        json={"room_id": 1, "user_id": 1, "start_time": "2026-01-20T10:00:00", "end_time": "2026-01-20T12:00:00"},
    )
    assert response.status_code == 200
    booking = response.json()
    assert booking["room_id"] == 1
    assert booking["user_id"] == 1

    # Retrieve the booking
    response = client.get(f"{API_URL}/bookings/{booking['id']}")
    assert response.status_code == 200
    retrieved_booking = response.json()
    assert retrieved_booking == booking