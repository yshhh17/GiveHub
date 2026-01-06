from fastapi import FastAPI, HTTPException, status, Depends, APIRouter, Request
import hmac
import hashlib
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
import logging
from ..services.email import send_payment_done_email
from ..core.rate_limit import limiter

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/donations",
    tags=["donations"]
)

@router.post("/create-order", response_model=PayPalOrderResponse)
@limiter.limit("2/minute")
async def create_donation_order(request: Request,donation: DonationCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        logger.info(f"User {current_user.id} creating donation order for ${donation.amount}")

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

        logger.info(f"Order created: {order['id']}")

        return {
            "order_id": order["id"],
            "status": order["status"],
            "approval_url": approval_url
        }
    except Exception as e:
        logger.error(f"Error creating order: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=str(e))

@router.post("/capture-order", response_model=DonationResponse)
@limiter.limit("10/minute")
async def capture_donation_order(request: Request,capture_request: PayPalCaptureRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    try:
        logger.info(f"created a capture order request for user: {current_user.id}")

        result = await paypal_service.capture_order(capture_request.order_id)

        if result["status"] != "COMPLETED":
            logger.error(f"order failed to capture")
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

        send_payment_done_email(current_user.email, donation.amount)

        logger.info(f"order captured successfully")

        return donation

    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=str(e))

@router.get("/my-donations", response_model=List[DonationResponse])
@limiter.limit("20/minute")
def get_my_donations(request: Request,skip: int = 0,limit: int = 10,db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    donations = db.query(Donation).filter(Donation.user_id == current_user.id).order_by(Donation.created_at.desc()).offset(skip).limit(limit).all()

    if not donations:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"no donations has been done yet")

    return donations

@router.get("/{donation_id}", response_model=DonationResponse)
@limiter.limit("20/minute")
def get_donation(request: Request,current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    donation = db.query(Donation).filter(Donation.id == donation_id, Donation.user_id == current_user.id).first()

    if not donation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"donation with {donation_id} not found")

    return donation

@router.get("/verify/{order_id}")
@limiter.limit("30/minute")
async def verify_order_status(request: Request,order_id: str, current_user: User = Depends(get_current_user)):
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

    @router.post("/paypal-webhook")
    async def paypal_webhook(request: Request, db: Session = Depends(get_db)):
        body = await request.body()
        headers = request.headers
        
        payload = await request.json()
        event_type = payload.get("event_type")
        
        if event_type == "PAYMENT.CAPTURE.COMPLETED":
            # Payment was captured
            order_id = payload["resource"]["supplementary_data"]["related_ids"]["order_id"]
            
            # Update donation in database
            donation = db.query(Donation).filter(
                Donation.payment_reference == order_id
            ).first()
            
            if donation and not donation.status:
                donation.status = True
                user = db.query(User).filter(User.id == donation.user_id).first()
                if user:
                    user.total_donated += donation.amount
                db.commit()
            
            return {"status": "success"}
        
        return {"status": "received"}