import httpx
import base64
from typing import Dict, Any, Optional
from fastapi import HTTPException
from ..core.config import settings

class PayPalService:
    def __init__(self):
        self.base_url = settings.paypal_api_base
        self.client_id = settings.paypal_client_id
        self.client_secret = settings.paypal_client_secret
        self._access_token:  Optional[str] = None
    
    async def get_access_token(self) -> str:
        """Get PayPal OAuth access token"""
        auth = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()
        
        headers = {
            "Authorization": f"Basic {auth}",
            "Content-Type":  "application/x-www-form-urlencoded"
        }
        
        data = "grant_type=client_credentials"
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/v1/oauth2/token",
                headers=headers,
                content=data
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Failed to get PayPal access token"
                )
            
            self._access_token = response.json()["access_token"]
            return self._access_token
    
    async def create_order(self, amount: float, currency: str = "USD") -> Dict[str, Any]: 
        if not self._access_token:
            await self.get_access_token()
        
        headers = {
            "Content-Type": "application/json",
            "Authorization":  f"Bearer {self._access_token}"
        }
        
        payload = {
            "intent": "CAPTURE",
            "purchase_units": [{
                "amount": {
                    "currency_code": currency,
                    "value": str(amount)
                },
                "description": "Donation"
            }],
            "application_context": {
                "brand_name": "Donation App",
                "locale": "en-US",
                "landing_page": "LOGIN",
                "shipping_preference":  "NO_SHIPPING",  # Important!  No address needed
                "user_action": "PAY_NOW",  # Important! Skip review page
                "return_url": "https://example.com/success",
                "cancel_url": "https://example.com/cancel"
            }
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.base_url}/v2/checkout/orders",
                headers=headers,
                json=payload
            )
            
            if response.status_code not in [200, 201]:  
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Failed to create PayPal order:  {response.text}"
                )
            
            return response.json()
    
    async def capture_order(self, order_id: str) -> Dict[str, Any]:
        """Capture/Complete a PayPal order"""
        if not self._access_token:
            await self.get_access_token()
        
        headers = {
            "Content-Type":  "application/json",
            "Authorization": f"Bearer {self._access_token}"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/v2/checkout/orders/{order_id}/capture",
                headers=headers
            )
            
            if response.status_code not in [200, 201]:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Failed to capture order: {response.text}"
                )
            
            return response.json()
    
    async def get_order_details(self, order_id: str) -> Dict[str, Any]:
        """Get order details"""
        if not self._access_token:
            await self.get_access_token()
        
        headers = {
            "Authorization": f"Bearer {self._access_token}"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/v2/checkout/orders/{order_id}",
                headers=headers
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Failed to get order details"
                )
            
            return response. json()

# Singleton instance
paypal_service = PayPalService()