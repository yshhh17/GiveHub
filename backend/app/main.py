from fastapi import FastAPI, Request, Depends
from sqlalchemy.orm import Session
from .db.database import Base, engine, get_db
from .db.models import User, Donation
from .routers import users, donations, webhook
from .core.rate_limit import limiter, rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
import logging
from fastapi.middleware.cors import CORSMiddleware
from .core.security import get_current_user
from .core.config import settings


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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        settings.frontend_url,
    ],
    allow_credentials=False,  # 🔑 IMPORTANT
    allow_methods=["*"],
    allow_headers=["*"],
)



app.state.limiter = limiter

app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

Base.metadata.create_all(bind=engine)

@app.get("/")
@limiter.limit("10/minute")
def greet(request: Request):
    return {"message": "Hello from server"}

@app.get("/me")
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current logged-in user's information"""
    return {
        "id": current_user.id,
        "name": current_user. name,
        "email": current_user.email,
        "created_at": current_user. created_at
    }

app.include_router(users.router)
app.include_router(donations.router)
app.include_router(webhook.router)