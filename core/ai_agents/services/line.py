import os
import httpx
import logging
import hashlib
import hmac
import base64
from typing import Dict, Any

logger = logging.getLogger(__name__)

class LineService:
    """Service for interacting with LINE Messaging API"""
    
    def __init__(self):
        self.channel_secret = os.getenv('LINE_CHANNEL_SECRET', '')
        self.channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', '')
        self.api_url = "https://api.line.me/v2/bot"
        
        if not self.channel_secret or not self.channel_access_token:
            logger.warning("LINE credentials not fully configured in environment variables.")
    
    def verify_webhook(self, body_str: str, signature: str) -> bool:
        """
        Verify the signature of the incoming webhook from LINE
        """
        if not self.channel_secret or not signature:
            return False
            
        hash = hmac.new(
            self.channel_secret.encode('utf-8'),
            body_str.encode('utf-8'),
            hashlib.sha256
        ).digest()
        
        expected_signature = base64.b64encode(hash).decode('utf-8')
        
        # compare_digest helps prevent timing attacks
        return hmac.compare_digest(signature, expected_signature)

    def reply_message(self, reply_token: str, message_text: str) -> Dict[str, Any]:
        """
        Reply to a user's message using the replyToken
        """
        if not self.channel_access_token:
            logger.error("Failed to send LINE message: Access Token is missing.")
            return {"error": "LINE service not configured properly."}
            
        headers = {
            "Authorization": f"Bearer {self.channel_access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "replyToken": reply_token,
            "messages": [
                {
                    "type": "text",
                    "text": message_text
                }
            ]
        }
        
        try:
            with httpx.Client() as client:
                response = client.post(
                    f"{self.api_url}/message/reply",
                    headers=headers,
                    json=payload,
                    timeout=10.0
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"LINE API HTTP error: {e.response.text}")
            return {"error": str(e), "details": e.response.text}
        except Exception as e:
            logger.error(f"LINE API generic error: {e}")
            return {"error": str(e)}
