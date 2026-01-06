from ..db.models import User, Donation
from ..db.database import get_db
from ..schemas.user import UserCreate, UserReturn, Token, VerifyOtp
from fastapi import FastAPI, Response, HTTPException, APIRouter, Depends, status, Request
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..core.security import hash_password, verify_password, create_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..services.otp import generate_otp, store_otp, redis_client
from ..services.email import send_otp_email
import asyncio
import logging
from ..core.rate_limit import limiter

logging = logging.getLogger(__name__)

router = APIRouter(
    tags=["users"]
)

@router.post("/register", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/hour")
async def create_user(request: Request,user: UserCreate, db: Session = Depends(get_db)):
    user.password = hash_password(user.password)
    new_user = User(name= user.name, email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    otp = generate_otp()
    await store_otp(user.email, otp)
    send_otp_email(user.email, otp)
    return {
        "message": "Registration successful! please verify your email",
        "email": user.email
    }

@router.post("/verify-email")
@limiter.limit("10/hour")
async def verify_otp(request: Request,data: VerifyOtp, db: Session = Depends(get_db)):
    stored_otp = await redis_client.get(f"otp:{data.email}")
    if not stored_otp:
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT,
        detail="OTP expired")
    if stored_otp != data.otp:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid OTP, Try again")

    user = db.query(User).filter(User.email == data.email).first()
    user.verified = True
    db.commit()

    redis_client.delete(f"otp:{data.email}")

    return {
        "message": "Email verified successfully"
    }

@router.post("/login", response_model=Token)
@limiter.limit("20/hour")
def user_login(request: Request,user_creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    current_user = db.query(User).filter(User.email == user_creds.username).first()
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    if not verify_password(user_creds.password, current_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    if not current_user.verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="email not verified")

    token = create_access_token({"user_id": current_user.id})

    return {"access_token": token, "token_type": "bearer"}