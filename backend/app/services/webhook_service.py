import requests
from typing import Dict
import logging
import json

logger = logging.getLogger(__name__)

class WebhookService: 
    """Service to verify PayPal webhook signatures"""
    
    async def verify_webhook_signature(
        self,
        webhook_id: str,
        headers:  Dict[str, str],
        body: str  # Changed from bytes to string
    ) -> bool:
        """
        Verify that the webhook request actually came from PayPal
        """
        try:
            # Extract signature headers
            transmission_id = headers.get("paypal-transmission-id")
            transmission_time = headers.get("paypal-transmission-time")
            cert_url = headers.get("paypal-cert-url")
            auth_algo = headers.get("paypal-auth-algo")
            transmission_sig = headers.get("paypal-transmission-sig")
            
            # Debug logging
            logger.info(f"Webhook ID: {webhook_id}")
            logger.info(f"Transmission ID: {transmission_id}")
            logger.info(f"Transmission Time: {transmission_time}")
            logger.info(f"Cert URL: {cert_url}")
            logger.info(f"Auth Algo: {auth_algo}")
            logger.info(f"Transmission Sig: {transmission_sig}")
            
            if not webhook_id: 
                logger.error("PAYPAL_WEBHOOK_ID is not set in environment variables!")
                return False
            
            if not all([transmission_id, transmission_time, cert_url, auth_algo, transmission_sig]):
                logger.error("Missing required webhook headers")
                logger.error(f"Headers received: {headers}")
                return False
            
            # Get PayPal settings
            from ..core.config import settings
            
            # Use PayPal's verification API
            verification_url = f"{settings.paypal_api_base}/v1/notifications/verify-webhook-signature"
            
            # Get access token
            from .paypal_service import paypal_service
            access_token = await paypal_service.get_access_token()
            
            # Parse body as JSON to re-serialize it
            # This ensures the format matches what PayPal expects
            try:
                webhook_event = json.loads(body) if isinstance(body, str) else json.loads(body.decode('utf-8'))
            except: 
                webhook_event = body
            
            verification_data = {
                "transmission_id": transmission_id,
                "transmission_time": transmission_time,
                "cert_url": cert_url,
                "auth_algo": auth_algo,
                "transmission_sig": transmission_sig,
                "webhook_id": webhook_id,
                "webhook_event": webhook_event
            }
            
            logger.info(f"Sending verification request to: {verification_url}")
            
            response = requests.post(
                verification_url,
                json=verification_data,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {access_token}"
                }
            )
            
            logger.info(f"Verification response status: {response.status_code}")
            logger.info(f"Verification response:  {response.text}")
            
            result = response.json()
            verification_status = result.get("verification_status")
            
            if verification_status == "SUCCESS":
                logger.info("Webhook signature verified successfully")
                return True
            else: 
                logger.warning(f"Webhook verification failed: {verification_status}")
                return False
                
        except Exception as e:
            logger.error(f"Error verifying webhook signature: {str(e)}", exc_info=True)
            return False

webhook_service = WebhookService()