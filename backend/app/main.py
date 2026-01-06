from fastapi import FastAPI, Request
from sqlalchemy.orm import Session
from .db.database import Base, engine, get_db
from .db.models import User, Donation
from .routers import users, donations, webhook
from .core.rate_limit import limiter, rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="GiveHub API",
    description="Donation platform with PayPal integration",
    version="1.0.0"
)

app.state.limiter = limiter

app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

Base.metadata.create_all(bind=engine)

@app.get("/")
@limiter.limit("10/minute")
def greet(request: Request):
    return {"message": "Hello from server"}

app.include_router(users.router)
app.include_router(donations.router)
app.include_router(webhook.router)