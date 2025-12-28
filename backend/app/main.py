from fastapi import FastAPI
from sqlalchemy.orm import Session
from .db.database import Base, engine, get_db
from .db.models import User, Donation
from .routers import users, donations


app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return {"message": "Hello from server"}

app.include_router(users.router)
app.include_router(donations.router)