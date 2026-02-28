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

    def reply_message(self, reply_token: str, messages) -> Dict[str, Any]:
        """
        Reply to a user's message using the replyToken
        Can accept a simple string or a list of message objects
        """
        if not self.channel_access_token:
            logger.error("Failed to send LINE message: Access Token is missing.")
            return {"error": "LINE service not configured properly."}
            
        if isinstance(messages, str):
            messages = [{"type": "text", "text": messages}]
            
        headers = {
            "Authorization": f"Bearer {self.channel_access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "replyToken": reply_token,
            "messages": messages
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

    def _send_push(self, to_user_id: str, messages: list) -> Dict[str, Any]:
        """
        Helper method to send a push message to LINE API
        """
        if not self.channel_access_token:
            logger.error("Failed to send LINE message: Access Token is missing.")
            return {"error": "LINE service not configured properly."}
            
        headers = {
            "Authorization": f"Bearer {self.channel_access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "to": to_user_id,
            "messages": messages
        }
        
        try:
            with httpx.Client() as client:
                response = client.post(
                    f"{self.api_url}/message/push",
                    headers=headers,
                    json=payload,
                    timeout=10.0
                )
                response.raise_for_status()
                return response.json() if response.content else {"status": "success"}
        except httpx.HTTPStatusError as e:
            logger.error(f"LINE Push API HTTP error: {e.response.text}")
            return {"error": str(e), "details": e.response.text}
        except Exception as e:
            logger.error(f"LINE Push API generic error: {e}")
            return {"error": str(e)}

    def push_message(self, to_user_id: str, message_text: str) -> Dict[str, Any]:
        """
        Push a normal text message
        """
        messages = [
            {
                "type": "text",
                "text": message_text
            }
        ]
        return self._send_push(to_user_id, messages)

    def push_image_message(self, to_user_id: str, original_content_url: str, preview_image_url: str = None) -> Dict[str, Any]:
        """
        Push an image message. 
        Note: URLs must be HTTPS and JPEG/PNG format.
        """
        if not preview_image_url:
            preview_image_url = original_content_url
            
        messages = [
            {
                "type": "image",
                "originalContentUrl": original_content_url,
                "previewImageUrl": preview_image_url
            }
        ]
        return self._send_push(to_user_id, messages)

    def push_flex_message(self, to_user_id: str, alt_text: str, flex_contents: Dict[str, Any]) -> Dict[str, Any]:
        """
        Push a Flex message with custom rich layout
        """
        messages = [
            {
                "type": "flex",
                "altText": alt_text,
                "contents": flex_contents
            }
        ]
        return self._send_push(to_user_id, messages)
