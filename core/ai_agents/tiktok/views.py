import json
import logging
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
import hmac
import hashlib
from django.conf import settings
from .bot import TikTokGeminiBot

logger = logging.getLogger(__name__)

@csrf_exempt
def tiktok_webhook(request):
    """Webhook endpoint for TikTok API (if configured)"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
        
    try:
        # Currently we just handle basic health checks / replies
        # For actual webhook, TikTok sends specific verification structures
        payload = json.loads(request.body)
        logger.info(f"Received TikTok webhook: {payload}")
        
        # We can implement specific webhook logic here later if needed
        # For now, we'll just manually trigger comment processing
        
        return JsonResponse({'code': 0, 'message': 'success'})
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return JsonResponse({'error': str(e)}, status=500)

def verify_shop_webhook(data, signature):
    """Verify TikTok Shop webhook signature"""
    app_secret = getattr(settings, 'TIKTOK_SHOP_APP_SECRET', '')
    if not app_secret:
        logger.error("TIKTOK_SHOP_APP_SECRET not configured")
        return False
        
    mac = hmac.new(app_secret.encode('utf-8'), data, hashlib.sha256)
    return mac.hexdigest() == signature

@csrf_exempt
def tiktok_shop_webhook(request):
    """Webhook endpoint specifically for TikTok Shop (e.g., Order Status Change)"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
        
    try:
        # TikTok Shop usually explicitly sends the signature in the header
        signature = request.headers.get('X-Shop-Signature', '')
        raw_data = request.body
        
        # 1. Verify Signature
        if not verify_shop_webhook(raw_data, signature):
            logger.warning("Invalid TikTok Shop Webhook Signature")
            return JsonResponse({"message": "Invalid signature"}, status=401)
            
        # 2. Parse JSON Data
        payload = json.loads(request.body)
        event_type = payload.get("type")
        
        logger.info(f"Received TikTok Shop Event: {event_type}")

        # Example: Handle order status change
        if event_type == "ORDER_STATUS_CHANGE":
            order_data = payload.get("data", {})
            order_id = order_data.get("order_id")
            new_status = order_data.get("order_status")
            
            # 111 = AWAITING_SHIPMENT is commonly used
            if new_status == 111:
                logger.info(f"📦 ມີອໍເດີໃໝ່ເຂົ້າແລ້ວ! Order ID: {order_id}")
                # TODO: Optional - Add Line Notify, update inventory, or save to DB
                
        # Must return quickly for Webhook (TikTok requests < 3-5s response)
        return JsonResponse({"code": 0, "message": "success"})
        
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON mapping"}, status=400)
    except Exception as e:
        logger.error(f"TikTok Shop Webhook processing error: {e}")
        return JsonResponse({"error": str(e)}, status=500)

def force_check_comments(request):
    """Trigger the bot manually to check and reply to comments"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
        
    try:
        bot = TikTokGeminiBot()
        results = bot.process_new_comments()
        
        return JsonResponse({
            'status': 'success',
            'comments_processed': len(results),
            'results': results
        })
        
    except Exception as e:
        logger.error(f"Error checking comments manually: {e}")
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def post_tiktok_video(request):
    """
    ທົດສອບລະບົບໂພສວິດີໂອລົງ TikTok ໂດຍກົງ
    """
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
        
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
        
    try:
        data = json.loads(request.body)
        video_url = data.get("video_url")
        title = data.get("title", "ໂພສວິດີໂອໃໝ່ຈາກ Python For Laos! 🚀")
        
        if not video_url:
            return JsonResponse({'error': 'video_url is required'}, status=400)
            
        bot = TikTokGeminiBot()
        result = bot.post_video(
            video_url=video_url,
            title=title
        )
        
        return JsonResponse(result)
        
    except Exception as e:
        logger.error(f"TikTok Post Video Error: {e}")
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def tiktok_dashboard(request):
    """
    ໜ້າ Dashboard ແອັດມິນສຳລັບສະແດງລາຍງານໂຄສະນາ (Ads) ຈາກ TikTok Marketing API
    """
    bot = TikTokGeminiBot()
    
    # ຈະດຶງຂໍ້ມູນລາຍງານຕັ້ງແຕ່ວັນທີ 1 ເດືອນປັດຈຸບັນ
    from datetime import datetime
    now = datetime.now()
    start_date = now.replace(day=1).strftime('%Y-%m-%d')
    end_date = now.strftime('%Y-%m-%d')
    
    context = {
        'error': None,
        'report_data': [],
        'start_date': start_date,
        'end_date': end_date
    }
    
    try:
        data = bot.get_ads_report(start_date=start_date, end_date=end_date)
        context['report_data'] = data
    except Exception as e:
        context['error'] = str(e)
        
    return render(request, 'tiktok/dashboard.html', context)
