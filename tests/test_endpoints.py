import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

API_PREFIX = os.getenv("API_URL", "/api/v1")


def test_getclient(client):
    response = client.get(f"{API_PREFIX}/")
    assert response.status_code == 200


def test_create_booking_in_past(client):
    # Calculate yesterday's date
    yesterday = datetime.now() - timedelta(days=1)
    start_time = yesterday.replace(
        hour=10, minute=0, second=0, microsecond=0
    ).isoformat()
    end_time = yesterday.replace(hour=12, minute=0, second=0, microsecond=0).isoformat()

    # Attempt to create a booking in the past
    response = client.post(
        f"{API_PREFIX}/rooms/1/bookings/",
        json={"start_time": start_time, "end_time": end_time},
    )
    assert response.status_code == 400
    assert "past" in response.json()["detail"].lower()


def test_create_booking(client):
    # Calculate tomorrow's date
    tomorrow = datetime.now() + timedelta(days=1)
    start_time = tomorrow.replace(
        hour=10, minute=0, second=0, microsecond=0
    ).isoformat()
    end_time = tomorrow.replace(hour=12, minute=0, second=0, microsecond=0).isoformat()

    # Attempt to create a booking for tomorrow
    response = client.post(
        f"{API_PREFIX}/rooms/1/bookings/",
        json={"start_time": start_time, "end_time": end_time},
    )
    print("Response Detail:", response.json())
    assert response.status_code == 200
    assert response.json()["start_time"] == start_time


def test_get_bookings(client):
    response = client.get(f"{API_PREFIX}/rooms/1/bookings/")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_create_overlapping_booking(client):
    # Calculate tomorrow's date
    tomorrow = datetime.now() + timedelta(days=1)
    start_time = tomorrow.replace(
        hour=10, minute=0, second=0, microsecond=0
    ).isoformat()
    end_time = tomorrow.replace(hour=12, minute=0, second=0, microsecond=0).isoformat()

    # Create an initial booking
    client.post(
        f"{API_PREFIX}/rooms/1/bookings/",
        json={"start_time": start_time, "end_time": end_time},
    )

    # Attempt to create an overlapping booking
    overlapping_start = tomorrow.replace(
        hour=11, minute=0, second=0, microsecond=0
    ).isoformat()
    overlapping_end = tomorrow.replace(
        hour=13, minute=0, second=0, microsecond=0
    ).isoformat()
    response = client.post(
        f"{API_PREFIX}/rooms/1/bookings/",
        json={"start_time": overlapping_start, "end_time": overlapping_end},
    )
    assert response.status_code == 400
    assert "overlap" in response.json()["detail"].lower()


def test_delete_booking(client):
    response = client.delete(f"{API_PREFIX}/bookings/1")
    assert response.status_code == 200
