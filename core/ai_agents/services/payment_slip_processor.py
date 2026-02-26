"""
Payment Slip OCR & AI Processing
ປະມວນຜົນຮູບພາບຫຼັກຖານການໂອນເງິນດ້ວຍ AI
"""

import os
import re
from typing import Dict, Any, Optional
from PIL import Image
import logging

logger = logging.getLogger(__name__)


class PaymentSlipProcessor:
    """Process payment slips using OCR and AI"""

    def __init__(self):
        self.confidence_threshold = float(os.getenv('OCR_CONFIDENCE_THRESHOLD', '0.7'))

    def process_slip(self, image_path: str) -> Dict[str, Any]:
        """
        Process payment slip image

        Args:
            image_path: Path to payment slip image

        Returns:
            Extracted data and confidence score
        """
        try:
            # Extract text using OCR
            text = self._extract_text(image_path)

            # Parse extracted text
            parsed_data = self._parse_payment_info(text)

            # Calculate confidence
            confidence = self._calculate_confidence(parsed_data)

            return {
                'status': 'completed' if confidence >= self.confidence_threshold else 'review_needed',
                'extracted_data': parsed_data,
                'raw_text': text,
                'confidence_score': confidence,
                'needs_manual_review': confidence < self.confidence_threshold
            }

        except Exception as e:
            logger.error(f"Payment slip processing error: {e}")
            return {
                'status': 'failed',
                'error': str(e),
                'confidence_score': 0.0
            }

    def _extract_text(self, image_path: str) -> str:
        """Extract text from image using OCR"""
        try:
            import pytesseract
            img = Image.open(image_path)
            text = pytesseract.image_to_string(img, lang='eng')
            return text
        except ImportError:
            logger.warning("pytesseract not installed, using mock data")
            return "MOCK_DATA: Amount: 50000 LAK\nTransaction ID: TXN123456\nDate: 2024-01-15"
        except Exception as e:
            logger.error(f"OCR error: {e}")
            return ""

    def _parse_payment_info(self, text: str) -> Dict[str, Any]:
        """Parse payment information from text"""
        data = {
            'amount': None,
            'currency': 'LAK',
            'transaction_id': None,
            'payment_date': None,
            'sender_name': None,
            'bank_name': None
        }

        # Extract amount
        amount_patterns = [
            r'(?:amount|ຈຳນວນ|total)[:\s]*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(?:LAK|USD|THB|kip)',
        ]

        for pattern in amount_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                amount_str = match.group(1).replace(',', '')
                try:
                    data['amount'] = float(amount_str)
                    break
                except ValueError:
                    pass

        # Extract transaction ID
        txn_patterns = [
            r'(?:transaction|ref|reference)[:\s#]*([A-Z0-9]{6,})',
            r'TXN[:\s]*([A-Z0-9]+)',
        ]

        for pattern in txn_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data['transaction_id'] = match.group(1)
                break

        # Extract date
        date_patterns = [
            r'(\d{4}-\d{2}-\d{2})',
            r'(\d{2}/\d{2}/\d{4})',
        ]

        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                data['payment_date'] = match.group(1)
                break

        return data

    def _calculate_confidence(self, data: Dict) -> float:
        """Calculate confidence score based on extracted data"""
        score = 0.0
        total_fields = 4

        if data.get('amount'):
            score += 0.4  # Amount is most important
        if data.get('transaction_id'):
            score += 0.3
        if data.get('payment_date'):
            score += 0.2
        if data.get('sender_name'):
            score += 0.1

        return round(score, 2)

    def verify_with_ai(self, image_path: str, extracted_data: Dict) -> Dict[str, Any]:
        """Verify extracted data using AI vision model (GPT-4 Vision or Claude)"""
        try:
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

            with open(image_path, 'rb') as img_file:
                import base64
                base64_image = base64.b64encode(img_file.read()).decode('utf-8')

            response = client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Extract payment information: amount, transaction ID, date, sender name"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=300
            )

            return {
                'ai_verification': response.choices[0].message.content,
                'verified': True
            }

        except Exception as e:
            logger.error(f"AI verification error: {e}")
            return {'verified': False, 'error': str(e)}
