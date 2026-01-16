from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, Room, Booking

# Initialize FastAPI app
app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Room Booking API!"}

# CRUD Endpoints

# Create a new booking
@app.post("/bookings/")
def create_booking(room_id: int, start_time: str, end_time: str, db: Session = Depends(get_db)):
    booking = Booking(room_id=room_id, start_time=start_time, end_time=end_time)
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

# Read all bookings
@app.get("/bookings/")
def read_bookings(db: Session = Depends(get_db)):
    return db.query(Booking).all()

# Read bookings for a specific room by ID
@app.get("/rooms/{room_id}/bookings/")
def read_bookings_for_room(room_id: int, db: Session = Depends(get_db)):
    bookings = db.query(Booking).filter(Booking.room_id == room_id).all()
    if not bookings:
        raise HTTPException(status_code=404, detail="No bookings found for this room")
    return bookings

# Update a booking
@app.put("/bookings/{booking_id}")
def update_booking(booking_id: int, start_time: str, end_time: str, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    booking.start_time = start_time
    booking.end_time = end_time
    db.commit()
    db.refresh(booking)
    return booking

# Delete a booking
@app.delete("/bookings/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    db.delete(booking)
    db.commit()
    return {"detail": "Booking deleted"}

# Example endpoint: List all bookings for a room by ID
@app.get("/example/rooms/{room_id}/bookings/")
def example_list_bookings_for_room(room_id: int, db: Session = Depends(get_db)):
    return read_bookings_for_room(room_id, db)