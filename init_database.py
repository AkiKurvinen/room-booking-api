from app.db.database import Base, engine, SessionLocal
from app.models.room import Room
from app.models.booking import Booking
from datetime import datetime


# Initialize the database and add initial data
def init_db(session=None):
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Use provided session or create a new one
    own_session = False
    if session is None:
        session = SessionLocal()
        own_session = True

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
        if own_session:
            session.close()


if __name__ == "__main__":
    print("Initializing the database...")
    init_db()
    print("Database initialized successfully!")
