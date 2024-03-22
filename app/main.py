"""
This module initializes a FastAPI application and sets up CORS middleware.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routers import users, maps, restaurants, comments, diaries
# from app.models import database, engine
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await database.connect()
    yield
    # await database.disconnect()


app = FastAPI(
    title="Backend",
    description="Backend API for Restaurant Map",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust based on your frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Include Routers 
app.include_router(users.router)
# app.include_router(maps.router)
# app.include_router(restaurants.router)
# app.include_router(comments.router)
# app.include_router(diaries.router)

# Optional: Simple root endpoint to check API status
@app.get("/") 
async def root():
    return {"message": "Welcome to the API!"}


@app.get("/heartbeat")
async def heartbeat():
    return {"message": "Hello World"}
