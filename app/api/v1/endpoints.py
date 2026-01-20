from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models import Room, Booking
from app.schemas.booking import BookingCreate, Booking as BookingSchema
from typing import Generator, List
from datetime import datetime

router = APIRouter()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATE
@router.post("/rooms/{room_id}/bookings/", response_model=BookingSchema)
def create_booking_for_room(
    room_id: int, booking: BookingCreate, db: Session = Depends(get_db)
) -> Booking:
    # Ensure the room exists
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    # Ensure the booking time is not in the past
    if booking.start_time < datetime.now().isoformat():
        raise HTTPException(status_code=400, detail="Booking time cannot be in the past")

    # Check for overlapping bookings
    overlapping_booking = (
        db.query(Booking)
        .filter(
            Booking.room_id == room_id,
            Booking.start_time < booking.end_time,
            Booking.end_time > booking.start_time,
        )
        .first()
    )

    if overlapping_booking:
        raise HTTPException(
            status_code=400, detail="Booking times overlap with an existing booking"
        )

    # Create the booking tied to the room
    db_booking = Booking(
        start_time=booking.start_time, end_time=booking.end_time, room_id=room_id
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


# READ
@router.get("/")
def read_root() -> dict:
    return {"message": "Room Booking API is running"}


@router.get("/rooms/{room_id}/bookings/", response_model=List[BookingSchema])
def read_bookings_for_room(room_id: int, db: Session = Depends(get_db)) -> List[Booking]:
    bookings = db.query(Booking).filter(Booking.room_id == room_id).all()
    if not bookings:
        raise HTTPException(status_code=404, detail="No bookings found for this room")
    return bookings

# UPDATE
"""no endpoints"""


# DELETE
@router.delete("/bookings/{booking_id}", status_code=200)
def delete_booking(booking_id: int, db: Session = Depends(get_db)) -> dict:
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    db.delete(booking)
    db.commit()
    return {"message": "Booking deleted successfully"}
