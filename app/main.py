from fastapi import FastAPI
from app.api.v1.endpoints import router

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access environment variables
API_URL = os.getenv("API_URL", "/api/v1")  # Default to /api/v1 if not set
DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Initialize FastAPI app
app = FastAPI()

# Include API router
app.include_router(router, prefix=API_URL)
