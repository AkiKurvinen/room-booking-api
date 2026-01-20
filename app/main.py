from fastapi import FastAPI
from app.api.v1.endpoints import router

# Initialize FastAPI app
app = FastAPI()

# Include API router
app.include_router(router, prefix="/api/v1")
