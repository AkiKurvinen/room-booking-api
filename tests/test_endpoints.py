def test_getclient(client):
    response = client.get("/api/v1/")
    assert response.status_code == 200

def test_create_booking(client):
    response = client.post(
        "/api/v1/rooms/1/bookings/",
        json={"start_time": "2026-01-17T10:00:00", "end_time": "2026-01-17T12:00:00"},
    )
    assert response.status_code == 200
    assert response.json()["start_time"] == "2026-01-17T10:00:00"

def test_get_bookings(client):
    response = client.get("/api/v1/rooms/1/bookings/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_create_overlapping_booking(client):
    # Create an initial booking
    client.post(
        "/api/v1/rooms/1/bookings/",
        json={"start_time": "2026-01-17T10:00:00", "end_time": "2026-01-17T12:00:00"},
    )

    # Attempt to create an overlapping booking
    response = client.post(
        "/api/v1/rooms/1/bookings/",
        json={"start_time": "2026-01-17T11:00:00", "end_time": "2026-01-17T13:00:00"},
    )
    assert response.status_code == 400
    assert "overlap" in response.json()["detail"].lower()

def test_delete_booking(client):
    response = client.delete("/api/v1/bookings/1")
    assert response.status_code == 200