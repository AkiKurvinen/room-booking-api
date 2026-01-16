from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.booking import Room, Booking as BookingModel
from app.schemas.booking import BookingCreate, Booking as BookingSchema, Room

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE
@router.post("/rooms/{room_id}/bookings/", response_model=BookingSchema)
def create_booking_for_room(room_id: int, booking: BookingCreate, db: Session = Depends(get_db)):
    # Ensure the room exists
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    # Create the booking tied to the room
    db_booking = BookingModel(**booking.dict(), room_id=room_id)
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

# READ
@router.get("/")
def read_root():
    return {"message": "Room Booking API is running"}

@router.get("/rooms/{room_id}/bookings/", response_model=list[BookingSchema])
def read_bookings_for_room(room_id: int, db: Session = Depends(get_db)):
    bookings = db.query(BookingModel).filter(BookingModel.room_id == room_id).all()
    if not bookings:
        raise HTTPException(status_code=404, detail="No bookings found for this room")
    return bookings

# UPDATE
    """no endpoints"""

# DELETE
@router.delete("/bookings/{booking_id}", status_code=204)
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(BookingModel).filter(BookingModel.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    db.delete(booking)
    db.commit()
    return None
