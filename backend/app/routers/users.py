from ..db.models import User, Donation
from ..db.database import get_db
from ..schemas.user import UserCreate, UserReturn, Token
from fastapi import FastAPI, Response, HTTPException, APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..core.security import hash_password, verify_password, create_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["users"]
)

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserReturn)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user.password = hash_password(user.password)
    new_user = User(name= user.name, email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
def user_login(user_creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    current_user = db.query(User).filter(User.email == user_creds.username).first()
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    if not verify_password(user_creds.password, current_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    token = create_access_token({"user_id": current_user.id})

    return {"access_token": token, "token_type": "bearer"}