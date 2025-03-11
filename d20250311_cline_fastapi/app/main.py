from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import todos
from app.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="TODO API",
    description="A simple TODO API built with FastAPI",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(todos.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to the TODO API. Visit /docs for the API documentation."}
