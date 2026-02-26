import os
import httpx
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class WhatsAppService:
    """Service for interacting with WhatsApp Cloud API"""
    
    def __init__(self):
        self.access_token = os.getenv('WHATSAPP_ACCESS_TOKEN')
        self.phone_number_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
        self.verify_token = os.getenv('WHATSAPP_VERIFY_TOKEN')
        self.api_version = os.getenv('WHATSAPP_VERSION', 'v18.0')
        
        if not self.access_token or not self.phone_number_id:
            logger.warning("WhatsApp credentials not fully configured in environment variables.")
            
        self.base_url = f"https://graph.facebook.com/{self.api_version}/{self.phone_number_id}"
        
    def send_message(self, to_phone_number: str, message_text: str) -> Dict[str, Any]:
        """
        Send a text message to a WhatsApp number.
        
        Args:
            to_phone_number: Phone number with country code (e.g., '85620XXXXXXXX'). Needs to be exactly what WhatsApp expects.
            message_text: The text message to send
            
        Returns:
            Dict containing the API response
        """
        if not self.access_token or not self.phone_number_id:
            logger.error("Failed to send WhatsApp message: Credentials are not configured.")
            return {"error": "WhatsApp service not configured properly."}
            
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to_phone_number,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": message_text
            }
        }
        
        try:
            # Use explicit httpx client like other services
            with httpx.Client() as client:
                response = client.post(
                    f"{self.base_url}/messages",
                    headers=headers,
                    json=payload,
                    timeout=10.0
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"WhatsApp API HTTP error: {e.response.text}")
            return {"error": str(e), "details": e.response.text}
        except Exception as e:
            logger.error(f"WhatsApp API generic error: {e}")
            return {"error": str(e)}
