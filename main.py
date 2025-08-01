from fastapi import FastAPI
from src.app.api.endpoints import users

app = FastAPI(
    title="Personal Tracker API",
    description="An API for tracking personal goals and tasks.",
    version="0.1.0",
)

app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Personal Tracker API!"}