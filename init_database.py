from app.db.database import Base, engine, SessionLocal
from app.db.database import Room, Booking
from datetime import datetime


# Initialize the database and add initial data
def init_db():
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Create a new session
    session = SessionLocal()

    try:
        # Add initial data
        room = Room(id=1, name="neukkari")
        booking = Booking(
            id=1, room_id=1, start_time=datetime.now(), end_time=datetime.now()
        )

        session.add(room)
        session.add(booking)
        session.commit()
    finally:
        session.close()


if __name__ == "__main__":
    print("Initializing the database...")
    init_db()
    print("Database initialized successfully!")
