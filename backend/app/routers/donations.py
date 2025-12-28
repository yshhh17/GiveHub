from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..db.models import Donation, User
from ..schemas.donation import (
    DonationCreate, 
    DonationResponse, 
    PayPalOrderResponse,
    PayPalCaptureRequest
)
from ..core.security import get_current_user
from ..services.paypal_service import paypal_service
from typing import List

router = APIRouter(
    prefix="/donations",
    tags=["donations"]
)

@router.post("/create-order", response_model=PayPalOrderResponse)
async def create_donation_order(donation: DonationCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        order = await paypal_service.create_order(
        amount=donation.amount,
        currency="USD"
        )

        approval_url = None
        for link in order.get("links", []):
            if link.get("rel") == "approve":
                approval_url = link.get("href")
                break
        
        new_donation = Donation(
            user_id = current_user.id,
            amount = donation.amount,
            status = False,
            payment_reference=order["id"]
        )
        db.add(new_donation)
        db.commit()
        db.refresh(new_donation)

        return {
            "order_id": order["id"],
            "status": order["status"],
            "approval_url": approval_url
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=str(e))

@router.post("/capture-order", response_model=DonationResponse)
async def capture_donation_order(capture_request: PayPalCaptureRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    try:
        result = await paypal_service.capture_order(capture_request.order_id)

        if result["status"] != "COMPLETED":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment capture Failed")

        donation = db.query(Donation).filter(Donation.payment_reference == capture_request.order_id, Donation.user_id == current_user.id).first()

        if not donation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="Donation not found")
        
        donation.status = True

        current_user.total_donated += donation.amount

        db.commit()
        db.refresh(donation)

        return donation

    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=str(e))

@router.get("/my-donations", response_model=List[DonationResponse])
def get_my_donations(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    donations = db.query(Donation).filter(Donation.user_id == current_user.id).all()
    return donations

@router.get("/{donation_id}", response_model=DonationResponse)
def get_donation(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    donation = db.query(Donation).filter(Donation.id == donation_id, Donation.user_id == current_user.id).first()

    if not donation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"donation with {donation_id} not found")

    return donation

@router.get("/verify/{order_id}")
async def verify_order_status(order_id: str, current_user: User = Depends(get_current_user)):
    try:
        order_details = await paypal_service.get_order_details(order_id)
        return {
            "order_id": order_id,
            "status": order_details.get("status"),
            "details": order_details
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=str(e))