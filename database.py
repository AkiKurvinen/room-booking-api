from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# SQLite database URL
DATABASE_URL = "sqlite:///./room_booking.db"

# Create the database engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Define the Room model
class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

# Define the Booking model
class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

# Initialize the database and add initial data
def init_db():
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Create a new session
    session = SessionLocal()

    try:
        # Add initial data
        room = Room(id=1, name="neukkari")
        booking = Booking(id=1, room_id=1, start_time=datetime.now(), end_time=datetime.now())

        session.add(room)
        session.add(booking)
        session.commit()
    finally:
        session.close()