from fastapi import APIRouter, Request, HTTPException, Depends, status
from sqlalchemy.orm import Session
import logging
import json

from ..db.database import get_db
from ..db.models import Donation, User
from ..services.webhook_service import webhook_service
from ..services.email import send_payment_done_email
from ..core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/webhooks",
    tags=["webhooks"]
)

@router.post("/paypal")
async def paypal_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Handle incoming PayPal webhook events
    """
    print("PAYPAL WEBHOOK RECEIVED")

    try:
        body = await request.body()
        body_str = body.decode("utf-8")
        headers = dict(request.headers)

        logger.info("Received PayPal webhook")
        logger.info(f"Event payload preview: {body_str[:200]}")

        event_data = json.loads(body_str)
        event_type = event_data.get("event_type")
        resource = event_data.get("resource", {})


        if not settings.paypal_webhook_id:
            logger.warning("PAYPAL_WEBHOOK_ID not set — skipping verification")
        else:
            is_valid = await webhook_service.verify_webhook_signature(
                webhook_id=settings.paypal_webhook_id,
                headers=headers,
                body=body_str
            )

            if not is_valid:
                logger.error("Invalid PayPal webhook signature")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid webhook signature"
                )

        if event_type == "PAYMENT.CAPTURE.COMPLETED":
            await handle_payment_completed(resource, db)

        elif event_type == "CHECKOUT.ORDER.APPROVED":
            await handle_order_approved(resource, db)

        elif event_type == "PAYMENT.CAPTURE.REFUNDED":
            await handle_payment_refunded(resource, db)

        elif event_type == "PAYMENT.CAPTURE.DENIED":
            await handle_payment_denied(resource, db)

        else:
            logger.info(f"Unhandled PayPal event type: {event_type}")

        print("Webhook processed successfully")

        return {
            "status": "success",
            "event_type": event_type
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error processing PayPal webhook", exc_info=True)
        return {"status": "error", "message": str(e)}


async def handle_order_approved(resource: dict, db: Session):
    try:
        order_id = resource.get("id")
        logger.info(f"Order approved: {order_id}")
    except Exception as e:
        logger.error("Error handling order approved", exc_info=True)


async def handle_payment_completed(resource: dict, db: Session):
    try:
        order_id = None

        if "supplementary_data" in resource:
            order_id = resource.get("supplementary_data", {}) \
                               .get("related_ids", {}) \
                               .get("order_id")

        if not order_id:
            order_id = resource.get("id")

        if not order_id:
            logger.error("Could not extract order_id from webhook")
            return

        logger.info(f"Processing completed payment for order {order_id}")

        donation = db.query(Donation).filter(
            Donation.payment_reference == order_id
        ).first()

        if not donation:
            logger.error(f"No donation found for order {order_id}")
            return

        if not donation.status:
            donation.status = True

            user = db.query(User).filter(User.id == donation.user_id).first()
            if user:
                user.total_donated += donation.amount
                send_payment_done_email(user.email, donation.amount)

            db.commit()
            logger.info(f"Donation {donation.id} marked as completed")

    except Exception:
        db.rollback()
        logger.error("Error handling completed payment", exc_info=True)


async def handle_payment_refunded(resource: dict, db: Session):
    try:
        order_id = resource.get("supplementary_data", {}) \
                           .get("related_ids", {}) \
                           .get("order_id")

        if not order_id:
            logger.error("Could not extract order_id from refund webhook")
            return

        donation = db.query(Donation).filter(
            Donation.payment_reference == order_id
        ).first()

        if donation and donation.status:
            donation.status = False
            user = db.query(User).filter(User.id == donation.user_id).first()
            if user:
                user.total_donated -= donation.amount

            db.commit()
            logger.info(f"Donation {donation.id} refunded")

    except Exception:
        db.rollback()
        logger.error("Error handling refund webhook", exc_info=True)


async def handle_payment_denied(resource: dict, db: Session):
    order_id = resource.get("id")
    logger.warning(f"Payment denied for order {order_id}")
