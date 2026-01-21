from fastapi import FastAPI
from app.api.v1.api import api_router
from dotenv import load_dotenv
import os

load_dotenv()

API_URL = os.getenv("API_URL", "/api/v1")
DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

app = FastAPI(
    title="Room Booking API",
    description="API for managing room bookings",
    version="1.0.0",
)

app.include_router(api_router, prefix="/api/v1")
