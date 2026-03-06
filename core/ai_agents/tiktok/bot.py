import requests
import google.generativeai as genai
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class TikTokGeminiBot:
    def __init__(self):
        # API Keys - Expected to be set in Django Settings from .env
        self.tiktok_access_token = getattr(settings, 'TIKTOK_ACCESS_TOKEN', '')
        self.tiktok_advertiser_id = getattr(settings, 'TIKTOK_ADVERTISER_ID', '')
        self.gemini_api_key = getattr(settings, 'GEMINI_API_KEY', '')
        
        # Configure Gemini
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self._init_model()
            
    def _init_model(self):
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "max_output_tokens": 150,
        }
        
        system_instruction = """
        ທ່ານຄືແອັດມິນເວັບໄຊທ໌ Python for Laos ທີ່ຕອບຄອມເມັ້ນໃນ TikTok.
        ໜ້າທີ່: ຕອບຄອມເມັ້ນລູກຄ້າໃຫ້ເປັນທຳມະຊາດທີ່ສຸດ ແລະ ເປັນກັນເອງ.
        ສະໄຕລ໌: ໃຊ້ພາສາລາວແບບໄວລຸ້ນ ຫຼື ພາສາເວົ້າທີ່ສຸພາບ ມີຫາງສຽງ "ເດີ", "ຄຮັບ", "ຈ້າ".
        ກົດເຫຼັກ:
        1. ຕອບສັ້ນໆ ໜ້ອຍກວ່າ 2 ປະໂຫຍກ.
        2. ໃຊ້ອີໂມຈິ 1-2 ຕົວ.
        3. ຖ້າຖາມກ່ຽວກັບຄອດຮຽນໃຫ້ນຳສະເໜີເວັບ pythonforlaos.com.
        4. ບໍ່ຕ້ອງພິມຂໍ້ຄວາມທັກທາຍຍາວໆ.
        """
        
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            system_instruction=system_instruction
        )
        
    def generate_reply(self, comment_text):
        """ໃຊ້ Gemini ສ້າງຂໍ້ຄວາມຕອບກັບ"""
        if not hasattr(self, 'model'):
            logger.warning("Gemini model not initialized.")
            return "ຂອບໃຈທີ່ສົນໃຈເດີ! ຕິດຕໍ່ສອບຖາມເພີ່ມເຕີມໃນ Inbox ໄດ້ເລີຍຄຮັບ ✨"
            
        try:
            # Fetch some recommended courses to give context to Gemini
            from courses.models import Course
            courses = Course.objects.filter(status='published').order_by('-is_featured', '-total_students')[:3]
            course_info = ""
            if courses:
                course_info = "ຄອສຮຽນທີ່ແນະນຳປະຈຸບັນມີ:\n" + "\n".join([f"- {c.title} ({'Free/ຟຣີ' if c.is_free else 'Paid/ມີຄ່າໃຊ້ຈ່າຍ'})" for c in courses])
                
            prompt = f"ຜູ້ໃຊ້ຄອມເມັ້ນວ່າ: '{comment_text}' ຊ່ວຍຕອບກັບແດ່.\n\n{course_info}"
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            logger.error(f"Gemini Error: {e}")
            return "ຂອບໃຈທີ່ສົນໃຈເດີ! ຕິດຕໍ່ສອບຖາມເພີ່ມເຕີມໃນ Inbox ໄດ້ເລີຍຄຮັບ ✨"

    def get_comments(self, page_size=10):
        """ດຶງຄອມເມັ້ນທີ່ຍັງບໍ່ທັນຕອບຈາກ TikTok"""
        if not self.tiktok_access_token or not self.tiktok_advertiser_id:
            logger.error("TikTok credentials not configured properly.")
            return []
            
        url = "https://business-api.tiktok.com/open_api/v1.3/ad_comment/get/"
        headers = {"Access-Token": self.tiktok_access_token}
        params = {
            "advertiser_id": self.tiktok_advertiser_id,
            "page_size": page_size,
            "is_replied": False  # Only get unreplied comments
        }
        
        try:
            res = requests.get(url, headers=headers, params=params)
            res.raise_for_status()
            data = res.json()
            if data.get("code") == 0:
                return data.get("data", {}).get("list", [])
            else:
                logger.error(f"TikTok API Error: {data.get('message')}")
                return []
        except Exception as e:
            logger.error(f"Failed to fetch TikTok comments: {e}")
            return []

    def send_reply(self, comment_id, reply_text):
        """ສົ່ງຂໍ້ຄວາມຕອບກັບໄປຍັງ TikTok"""
        if not self.tiktok_access_token or not self.tiktok_advertiser_id:
            return {"code": -1, "message": "Missing credentials"}
            
        url = "https://business-api.tiktok.com/open_api/v1.3/ad_comment/reply/"
        headers = {
            "Access-Token": self.tiktok_access_token,
            "Content-Type": "application/json"
        }
        payload = {
            "advertiser_id": self.tiktok_advertiser_id,
            "comment_id": comment_id,
            "text": reply_text
        }
        
        try:
            res = requests.post(url, headers=headers, json=payload)
            res.raise_for_status()
            return res.json()
        except Exception as e:
            logger.error(f"Failed to send TikTok reply: {e}")
            return {"code": -1, "message": str(e)}

    def process_new_comments(self):
        """ດຶງຄອມເມັ້ນໃໝ່ ແລະ ຕອບກັບອັດຕະໂນມັດ"""
        results = []
        comments = self.get_comments()
        
        for comment in comments:
            comment_id = comment.get('id')
            comment_text = comment.get('text')
            
            # Generate smart reply
            ai_reply = self.generate_reply(comment_text)
            
            # Send reply
            response = self.send_reply(comment_id, ai_reply)
            
            success = response.get("code") == 0
            results.append({
                "comment_id": comment_id,
                "original_text": comment_text,
                "ai_reply": ai_reply,
                "success": success,
                "api_response": response
            })
            
            if success:
                logger.info(f"Replied to comment {comment_id} successfully.")
            else:
                logger.error(f"Failed to reply to comment {comment_id}: {response.get('message')}")
                
        return results

    def post_video(self, video_url, title, privacy_level="PUBLIC_TO_EVERYONE", disable_comment=False):
        """
        ລະບົບໂພສວິດີໂອລົງ TikTok ໂດຍກົງ (Direct Post API)
        - `video_url`: URL ຂອງວິດີໂອທີ່ຕ້ອງການໂພສ (ຕ້ອງເປັນ URL ທີ່ສາມາດເຂົ້າເຖິງໄດ້ຈາກອິນເຕີເນັດ)
        - `title`: ແຄັບຊັ່ນຂອງວິດີໂອ
        - `privacy_level`: ລະດັບຄວາມເປັນສ່ວນຕົວ: PUBLIC_TO_EVERYONE, MUTUAL_FOLLOW_FRIENDS, FOLLOWER_OF_CREATOR, SELF_ONLY
        """
        # ສໍາລັບ Direct Post API, TikTok ຈະໃຊ້ Token ຂອງ TikTok for Developers (Login Kit/Share Kit)
        # ເຊິ່ງອາດຈະແຕກຕ່າງຈາກ Token ຂອງ Marketing API ແຕ່ໃນທີ່ນີ້ເຮົາຈະໃຊ້ OAUTH_TOKEN (Access Token)
        # ທີ່ໄດ້ຜ່ານການອະນຸຍາດ Scope `video.publish`
        
        # ສົມມຸດວ່າເຮົາໃຊ້ self.tiktok_access_token ເຊິ່ງມີ Scope ແລ້ວ
        if not self.tiktok_access_token:
            return {"error": "Missing TikTok Access Token"}
            
        url = "https://open.tiktokapis.com/v2/post/publish/video/init/"
        headers = {
            "Authorization": f"Bearer {self.tiktok_access_token}",
            "Content-Type": "application/json; charset=UTF-8"
        }
        data = {
            "post_info": {
                "title": title,
                "privacy_level": privacy_level,
                "disable_comment": disable_comment,
                "video_cover_timestamp_ms": 1000
            },
            "source_info": {
                "source": "PULL_FROM_URL",
                "video_url": video_url
            }
        }
        
        try:
            res = requests.post(url, headers=headers, json=data)
            res.raise_for_status()
            result = res.json()
            
            if result.get("error"):
                logger.error(f"TikTok Post Video Error: {result['error']}")
                return {"success": False, "error": result["error"]}
                
            return {
                "success": True, 
                "message": "Video publishing initialized successfully",
                "publish_id": result.get("data", {}).get("publish_id")
            }
        except Exception as e:
            logger.error(f"Failed to post video to TikTok: {e}")
            return {"success": False, "error": str(e)}

    # ==========================================
    # TikTok Business API (Marketing API) 
    # ==========================================
    def get_ads_report(self, start_date="2026-02-01", end_date="2026-02-28"):
        """ดึงข้อมูล Analytics ของโฆษณา (Ads Management)"""
        url = 'https://business-api.tiktok.com/open_api/v1.3/report/integrated/get/'
        headers = {
            'Access-Token': self.tiktok_access_token,
            'Content-Type': 'application/json'
        }
        params = {
            'advertiser_id': self.tiktok_advertiser_id,
            'report_type': 'BASIC',
            'data_level': 'AUCTION_AD',
            'dimensions': '["ad_id", "stat_time_day"]',
            'metrics': '["spend", "impressions", "clicks", "conversion"]',
            'start_date': start_date,
            'end_date': end_date
        }
        
        try:
            res = requests.get(url, headers=headers, params=params)
            res.raise_for_status()
            return res.json().get('data', {}).get('list', [])
        except Exception as e:
            logger.error(f"Failed to fetch ads report: {e}")
            return []

    # ==========================================
    # TikTok Shop API (v2)
    # ==========================================
    def get_shop_orders(self, shop_id, order_status=100):
        """ดึงข้อมูลคำสั่งซื้อ (Orders) จาก TikTok Shop"""
        import time
        import hmac
        import hashlib
        
        app_key = getattr(settings, 'TIKTOK_SHOP_APP_KEY', '')
        app_secret = getattr(settings, 'TIKTOK_SHOP_APP_SECRET', '')
        
        if not app_key or not app_secret:
            return {"error": "Shop API credentials missing"}
            
        timestamp = int(time.time())
        params = {
            "app_key": app_key,
            "timestamp": timestamp,
            "shop_id": shop_id,
            "version": "202309"
        }
        
        # Calculate signature
        sign_string = app_secret
        for key in sorted(params.keys()):
            sign_string += key + str(params[key])
        sign_string += app_secret
        
        sign = hmac.new(app_secret.encode('utf-8'), sign_string.encode('utf-8'), hashlib.sha256).hexdigest()
        
        url = f"https://open-api.tiktokglobalshop.com/api/orders/search?sign={sign}&access_token={self.tiktok_access_token}"
        payload = {"order_status": order_status}
        
        try:
            res = requests.post(url, params=params, json=payload)
            res.raise_for_status()
            return res.json()
        except Exception as e:
            logger.error(f"Failed to fetch shop orders: {e}")
            return {"error": str(e)}

    # ==========================================
    # Research API
    # ==========================================
    def search_research_videos(self, query):
        """เข้าถึงข้อมูลสาธารณะเพื่อการวิเคราะห์เทรนด์ (ต้องได้รับอนุมัติเฉพาะ)"""
        # Note: Research API endpoints typically require a separate Client Credential Grant token
        url = "https://open.tiktokapis.com/v2/research/video/query/?fields=id,create_time,like_count"
        headers = {
            "Authorization": f"Bearer {self.tiktok_access_token}",
            "Content-Type": "application/json"
        }
        data = {
            "query": {
                "and": [
                    {"operation": "IN", "field_name": "keyword", "field_values": [query]}
                ]
            },
            "max_count": 10
        }
        try:
            res = requests.post(url, headers=headers, json=data)
            res.raise_for_status()
            return res.json()
        except Exception as e:
            logger.error(f"Failed to search research API: {e}")
            return {"error": str(e)}
