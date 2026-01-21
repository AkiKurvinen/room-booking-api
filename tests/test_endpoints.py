import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

API_PREFIX = os.getenv("API_URL", "/api/v1")


def test_should_get_client(client):
    response = client.get(f"{API_PREFIX}/")
    assert response.status_code == 200


def test_should_not_create_booking_in_past(client):
    yesterday = datetime.now() - timedelta(days=1)
    start_time = yesterday.replace(
        hour=10, minute=0, second=0, microsecond=0
    ).isoformat()
    end_time = yesterday.replace(hour=12, minute=0, second=0, microsecond=0).isoformat()
    response = client.post(
        f"{API_PREFIX}/bookings/",
        json={"room_id": 1, "start_time": start_time, "end_time": end_time},
    )
    assert response.status_code == 400
    assert "past" in response.json()["detail"].lower()


def test_should_create_booking(client):
    tomorrow = datetime.now() + timedelta(days=1)
    start_time = tomorrow.replace(
        hour=10, minute=0, second=0, microsecond=0
    ).isoformat()
    end_time = tomorrow.replace(hour=12, minute=0, second=0, microsecond=0).isoformat()

    response = client.post(
        f"{API_PREFIX}/bookings/",
        json={"room_id": 1, "start_time": start_time, "end_time": end_time},
    )
    assert response.status_code == 200
    assert response.json()["start_time"] == start_time


def test_should_get_bookings_for_room(client):
    response = client.get(f"{API_PREFIX}/rooms/1/bookings/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_should_not_create_overlapping_booking(client):
    tomorrow = datetime.now() + timedelta(days=1)
    overlapping_start = tomorrow.replace(
        hour=11, minute=0, second=0, microsecond=0
    ).isoformat()
    overlapping_end = tomorrow.replace(
        hour=13, minute=0, second=0, microsecond=0
    ).isoformat()
    response = client.post(
        f"{API_PREFIX}/bookings/",
        json={
            "room_id": 1,
            "start_time": overlapping_start,
            "end_time": overlapping_end,
        },
    )
    assert response.status_code == 400
    assert "overlap" in response.json()["detail"].lower()


def test_should_not_create_booking_with_end_time_before_start_time(client):
    tomorrow = datetime.now() + timedelta(days=1)
    payload = {
        "room_id": 1,
        "start_time": tomorrow.replace(
            hour=10, minute=0, second=0, microsecond=0
        ).isoformat(),
        "end_time": tomorrow.replace(
            hour=9, minute=0, second=0, microsecond=0
        ).isoformat(),
    }

    response = client.post(f"{API_PREFIX}/bookings/", json=payload)

    assert response.status_code == 400
    assert "cannot be before" in response.json()["detail"].lower()


def test_should_delete_booking(client):
    response = client.delete(f"{API_PREFIX}/bookings/1")
    assert response.status_code == 200


def test_should_not_delete_non_existent_booking(client):
    response = client.delete(f"{API_PREFIX}/bookings/9999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
