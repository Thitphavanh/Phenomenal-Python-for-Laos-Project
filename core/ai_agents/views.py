"""
Views and API Endpoints for AI Agents
Django REST Framework ViewSets and APIViews
"""

from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.views import APIView
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import os
import json
import uuid
import logging
import re

from .models import (
    ChatConversation,
    ChatMessage,
    CourseAnalytics,
    PaymentSlipAnalysis,
    CourseRecommendation,
)
from .serializers import *
from .services.chatbot import MultiProviderChatbot, PythonLaosChatbot
from .services.analytics import CourseAnalyticsAgent, BusinessIntelligenceAgent
from .services.payment_slip_processor import PaymentSlipProcessor
from .services.recommendation import CourseRecommendationEngine

logger = logging.getLogger(__name__)


# ============================================
# CHATBOT VIEWS
# ============================================

class ChatAPIView(APIView):
    """API endpoint for chatbot"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Handle chat request"""
        serializer = ChatRequestSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        message = data['message']
        session_id = data.get('session_id') or str(uuid.uuid4())
        use_rag = data.get('use_rag', True)
        provider = data.get('provider', 'openai')
        
        try:
            # Get or create conversation
            conversation, created = ChatConversation.objects.get_or_create(
                session_id=session_id,
                defaults={'user': request.user if request.user.is_authenticated else None}
            )
            
            # Save user message
            ChatMessage.objects.create(
                conversation=conversation,
                role='user',
                content=message
            )
            
            # Get conversation history
            history = list(conversation.messages.values('role', 'content').order_by('created_at'))
            history_formatted = [{'role': m['role'], 'content': m['content']} for m in history[:-1]]
            
            # Get chatbot response
            chatbot = MultiProviderChatbot()
            response = chatbot.chat(
                message=message,
                provider=provider,
                conversation_history=history_formatted,
                use_rag=use_rag
            )
            
            # Save assistant message
            ChatMessage.objects.create(
                conversation=conversation,
                role='assistant',
                content=response['response'],
                metadata={
                    'sources': response.get('sources', []),
                    'tokens_used': response.get('tokens_used'),
                    'model': response.get('model'),
                    'provider': response.get('provider')
                }
            )
            
            # Prepare response
            response_data = {
                'response': response['response'],
                'session_id': session_id,
                'sources': response.get('sources', []),
                'tokens_used': response.get('tokens_used'),
                'model': response.get('model'),
                'provider': response.get('provider')
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Chat API error: {e}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


def chatbot_page(request):
    """Render chatbot UI page"""
    return render(request, 'ai_agents/chatbot.html')


# ============================================
# ANALYTICS VIEWS
# ============================================

class CourseAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for course analytics"""
    queryset = CourseAnalytics.objects.all()
    serializer_class = CourseAnalyticsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    @action(detail=False, methods=['post'])
    def generate(self, request):
        """Generate analytics for a course"""
        serializer = AnalyticsRequestSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        course_id = serializer.validated_data['course_id']
        
        try:
            agent = CourseAnalyticsAgent()
            analytics = agent.analyze_course(course_id)
            
            if 'error' in analytics:
                return Response(analytics, status=status.HTTP_404_NOT_FOUND)
            
            # Save to database
            from courses.models import Course
            course = Course.objects.get(id=course_id)
            
            # Mark previous analytics as not current
            CourseAnalytics.objects.filter(course=course).update(is_current=False)
            
            # Create new analytics
            analytics_obj = CourseAnalytics.objects.create(
                course=course,
                enrollment_prediction=analytics.get('predictions'),
                performance_insights=analytics.get('completion_analysis'),
                student_engagement_score=analytics.get('engagement_score', 0),
                completion_rate_prediction=analytics.get('basic_stats', {}).get('completion_rate', 0),
                recommendations='\n'.join(analytics.get('recommendations', [])),
                suggested_improvements=analytics.get('enrollment_trends'),
                is_current=True
            )
            
            response_serializer = CourseAnalyticsSerializer(analytics_obj)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            logger.error(f"Analytics generation error: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_course_analytics(request, course_id):
    """Get analytics for a specific course"""
    try:
        # Check if course exists
        from courses.models import Course
        course = get_object_or_404(Course, id=course_id)
        
        # Try to get existing latest analytics
        analytics = CourseAnalytics.objects.filter(
            course=course, 
            is_current=True
        ).first()
        
        # If no analytics or force refresh (optional), generate new
        if not analytics:
            agent = CourseAnalyticsAgent()
            result = agent.analyze_course(course_id)
            
            if 'error' in result:
                return Response(result, status=status.HTTP_404_NOT_FOUND)
                
            # Create new analytics object
            analytics = CourseAnalytics.objects.create(
                course=course,
                enrollment_prediction=result.get('enrollment_prediction'),
                student_engagement_score=result.get('engagement_score', 0),
                recommendations=result.get('recommendations', ''),
                is_current=True
            )
            
        serializer = CourseAnalyticsSerializer(analytics)
        return Response(serializer.data)
        
    except Exception as e:
        logger.error(f"Error fetching course analytics: {e}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def business_intelligence_report(request):
    """Generate monthly BI report"""
    try:
        agent = BusinessIntelligenceAgent()
        report = agent.generate_monthly_report()
        return Response(report, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"BI report error: {e}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============================================
# PAYMENT SLIP VIEWS
# ============================================

class PaymentSlipAnalysisViewSet(viewsets.ModelViewSet):
    """ViewSet for payment slip analysis"""
    queryset = PaymentSlipAnalysis.objects.all()
    serializer_class = PaymentSlipAnalysisSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter by user"""
        if self.request.user.is_staff:
            return PaymentSlipAnalysis.objects.all()
        return PaymentSlipAnalysis.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def analyze(self, request):
        """Analyze uploaded payment slip"""
        serializer = PaymentSlipUploadSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        image = serializer.validated_data['image']
        event_registration_id = serializer.validated_data.get('event_registration_id')
        
        try:
            # Save image
            analysis = PaymentSlipAnalysis.objects.create(
                image=image,
                user=request.user,
                status='processing'
            )
            
            # Process slip
            processor = PaymentSlipProcessor()
            result = processor.process_slip(analysis.image.path)
            
            # Update analysis
            analysis.extracted_data = result.get('extracted_data', {})
            analysis.amount = result.get('extracted_data', {}).get('amount')
            analysis.transaction_id = result.get('extracted_data', {}).get('transaction_id')
            analysis.payment_date = result.get('extracted_data', {}).get('payment_date')
            analysis.sender_name = result.get('extracted_data', {}).get('sender_name')
            analysis.confidence_score = result.get('confidence_score', 0)
            analysis.status = result.get('status', 'completed')
            
            if event_registration_id:
                from events.models import EventRegistration
                analysis.event_registration_id = event_registration_id
            
            analysis.save()
            
            response_serializer = PaymentSlipAnalysisSerializer(analysis)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            logger.error(f"Payment slip analysis error: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============================================
# RECOMMENDATION VIEWS
# ============================================

class CourseRecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for course recommendations"""
    queryset = CourseRecommendation.objects.all()
    serializer_class = CourseRecommendationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter by user"""
        return CourseRecommendation.objects.filter(
            user=self.request.user,
            is_active=True
        )
    
    @action(detail=False, methods=['post'])
    def generate(self, request):
        """Generate recommendations for current user"""
        serializer = RecommendationRequestSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        limit = serializer.validated_data.get('limit', 5)
        
        try:
            engine = CourseRecommendationEngine()
            recommendations = engine.recommend_for_user(request.user, limit=limit)
            
            # Save recommendations to database
            CourseRecommendation.objects.filter(user=request.user).update(is_active=False)
            
            for rec in recommendations:
                CourseRecommendation.objects.create(
                    user=request.user,
                    recommended_course=rec['course'],
                    relevance_score=rec['score'],
                    reason=rec['reason'],
                    based_on={'method': rec['method']},
                    is_active=True
                )
            
            # Get fresh data
            saved_recs = CourseRecommendation.objects.filter(
                user=request.user,
                is_active=True
            ).order_by('-relevance_score')
            
            response_serializer = CourseRecommendationSerializer(saved_recs, many=True)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Recommendation generation error: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============================================
# UTILITY VIEWS
# ============================================

@api_view(['GET'])
def ai_status(request):
    """Check AI services status"""
    chatbot = MultiProviderChatbot()
    
    return Response({
        'available_providers': chatbot.get_available_providers(),
        'vector_db_status': 'active',
        'services': {
            'chatbot': True,
            'analytics': True,
            'payment_processor': True,
            'recommendations': True
        }
    })


@login_required
def analytics_dashboard(request):
    """Render analytics dashboard"""
    return render(request, 'ai_agents/analytics_dashboard.html')


# ============================================
# WHATSAPP WEBHOOK VIEWS
# ============================================

from .services.whatsapp import WhatsAppService

class WhatsAppWebhookView(APIView):
    """Webhook for receiving and responding to WhatsApp messages"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Handle Webhook Verification requested by Meta"""
        verify_token = os.getenv('WHATSAPP_VERIFY_TOKEN')
        
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')
        
        if mode and token:
            if mode == 'subscribe' and token == verify_token:
                logger.info("WhatsApp WEBHOOK_VERIFIED")
                return HttpResponse(challenge, status=200)
            else:
                return HttpResponseForbidden()
                
        return HttpResponse("Invalid Request", status=400)
        
    def post(self, request):
        """Handle incoming WhatsApp messages"""
        try:
            body = request.data
            
            # Check if this is a WhatsApp API event
            if body.get('object') == 'whatsapp_business_account':
                for entry in body.get('entry', []):
                    for change in entry.get('changes', []):
                        value = change.get('value', {})
                        messages = value.get('messages', [])
                        
                        if messages:
                            # We got a message!
                            message = messages[0]
                            phone_number = message['from']  # Sender's phone number
                            message_type = message.get('type')
                            
                            if message_type == 'text':
                                message_text = message['text']['body']
                                
                                # Process with AI Chatbot
                                chatbot = MultiProviderChatbot()
                                response = chatbot.chat(
                                    message=message_text,
                                    provider='gemini' # Fallback default
                                )
                                
                                ai_response = response.get('response', 'ຂໍອະໄພ, ຂ້ອຍບໍ່ສາມາດຕອບໄດ້ໃນຂະນະນີ້.')
                                
                                # Send response back via WhatsApp
                                wa_service = WhatsAppService()
                                wa_service.send_message(phone_number, ai_response)
                                
                return HttpResponse("EVENT_RECEIVED", status=200)
            
            return HttpResponse("Not a WhatsApp API event", status=404)
            
        except Exception as e:
            logger.error(f"WhatsApp Webhook error: {e}")
            return HttpResponse("Error processing request", status=500)


# ============================================
# LINE INTEGRATION VIEWS
# ============================================

from .services.line import LineService

def line_login_page(request):
    """Render LINE Login/LIFF UI page"""
    return render(request, 'ai_agents/line_login.html')

class LineWebhookView(APIView):
    """Webhook for receiving and responding to LINE messages"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Handle incoming LINE messages"""
        line_service = LineService()
        
        # Security: Verify that the request is actually from LINE
        signature = request.META.get('HTTP_X_LINE_SIGNATURE', '')
        body = request.body.decode('utf-8')
        
        if not line_service.verify_webhook(body, signature):
            logger.warning("Invalid LINE webhook signature")
            return HttpResponseForbidden("Invalid LINE signature")
            
        try:
            events = request.data.get('events', [])
            
            for event in events:
                # Handle text messages
                if event.get('type') == 'message' and event.get('message', {}).get('type') == 'text':
                    reply_token = event.get('replyToken')
                    user_id = event.get('source', {}).get('userId')
                    message_text = event.get('message', {}).get('text')
                    
                    if reply_token and message_text:
                        # Process user message with AI
                        chatbot = MultiProviderChatbot()
                        # Set use_rag=False to speed up the response significantly 
                        # avoiding the synchronous delay of downloading/processing models during webhook.
                        response = chatbot.chat(
                            message=message_text,
                            provider='gemini', # Default fallback
                            use_rag=True
                        )
                        
                        ai_response = response.get('response', 'ຂໍອະໄພ, ຂ້ອຍບໍ່ສາມາດຕອບໄດ້ໃນຂະນະນີ້.')
                        
                        # Clean up unsupported formatting for LINE Chat
                        ai_response = re.sub(r'#{1,3}\s+', '', ai_response) # remove ### Headers
                        ai_response = re.sub(r'\*\*(.*?)\*\*', r'\1', ai_response) # remove bold **text**
                        ai_response = re.sub(r'_(.*?)_', r'\1', ai_response) # remove italics _text_
                        ai_response = re.sub(r'-{3,}', '\n', ai_response) # remove --- separators
                        
                        messages_to_send = [
                            {"type": "text", "text": ai_response}
                        ]
                        
                        # ----------------------------------------------------
                        # COURSE FLEX MESSAGE LOGIC
                        # ----------------------------------------------------
                        keywords = ['ຄອສ', 'ຮຽນ', 'course', 'ສົນໃຈ']
                        if any(kw in message_text.lower() for kw in keywords):
                            try:
                                from courses.models import Course
                                
                                # Fetch latest 5 published courses
                                courses = Course.objects.filter(status='published').order_by('-created_at')[:5]
                                if courses:
                                    from django.conf import settings
                                    import os
                                    
                                    # Fallback base URL for local development/ngrok
                                    base_url = os.getenv('SITE_URL', f"https://{request.get_host()}")
                                    
                                    bubbles = []
                                    for course in courses:
                                        if course.cover_image:
                                            # Using absolute URL
                                            cover_url = f"{base_url}{course.cover_image.url}"
                                        else:
                                            cover_url = "https://via.placeholder.com/600x400.png?text=Python+Course"
                                            
                                        course_url = f"{base_url}{course.get_absolute_url()}"
                                        
                                        price_text = f"${course.price}" if course.price > 0 else "Free / ຟຣີ"
                                        
                                        bubbles.append({
                                            "type": "bubble",
                                            "size": "mega",
                                            "hero": {
                                                "type": "image",
                                                "url": cover_url,
                                                "size": "full",
                                                "aspectRatio": "20:13",
                                                "aspectMode": "cover"
                                            },
                                            "body": {
                                                "type": "box",
                                                "layout": "vertical",
                                                "paddingAll": "20px",
                                                "contents": [
                                                    {
                                                        "type": "text",
                                                        "text": course.title[:40] + ("..." if len(course.title) > 40 else ""),
                                                        "weight": "bold",
                                                        "size": "md",
                                                        "wrap": True,
                                                        "maxLines": 2
                                                    },
                                                    {
                                                        "type": "text",
                                                        "text": price_text,
                                                        "color": "#1DB446",
                                                        "size": "sm",
                                                        "weight": "bold",
                                                        "margin": "md"
                                                    }
                                                ]
                                            },
                                            "footer": {
                                                "type": "box",
                                                "layout": "vertical",
                                                "spacing": "sm",
                                                "paddingAll": "20px",
                                                "contents": [
                                                    {
                                                        "type": "button",
                                                        "style": "primary",
                                                        "color": "#1DB446",
                                                        "action": {
                                                            "type": "uri",
                                                            "label": "ເບິ່ງລາຍລະອຽດ",
                                                            "uri": course_url
                                                        }
                                                    }
                                                ]
                                            }
                                        })
                                        
                                    messages_to_send.append({
                                        "type": "flex",
                                        "altText": "ລາຍການຄອສຮຽນທັງໝົດແບບ Flex",
                                        "contents": {
                                            "type": "carousel",
                                            "contents": bubbles
                                        }
                                    })
                            except Exception as e:
                                logger.error(f"Failed to generate course flex message: {e}")
                        
                        # Reply back to LINE user
                        line_service.reply_message(reply_token, messages_to_send)
                        
            return HttpResponse("OK", status=200)
            
        except Exception as e:
            logger.error(f"LINE Webhook error: {e}")
            return HttpResponse("Error processing request", status=500)


class LinePushMessageView(APIView):
    """API endpoint to push different types of messages to a specific LINE user"""
    permission_classes = [AllowAny] # Allow testing without token (can be reverted later)
    
    def post(self, request):
        to_user_id = request.data.get('to')
        msg_type = request.data.get('type', 'text') # default to text message
        
        if not to_user_id:
            return Response({'error': '"to" field is required.'}, status=status.HTTP_400_BAD_REQUEST)
            
        line_service = LineService()
        result = {}
        
        if msg_type == 'text':
            message_text = request.data.get('text')
            if not message_text:
                return Response({'error': '"text" field is required for text type.'}, status=status.HTTP_400_BAD_REQUEST)
            result = line_service.push_message(to_user_id, message_text)
            
        elif msg_type == 'image':
            original_url = request.data.get('original_content_url')
            preview_url = request.data.get('preview_image_url')
            if not original_url:
                return Response({'error': '"original_content_url" field is required for image type.'}, status=status.HTTP_400_BAD_REQUEST)
            result = line_service.push_image_message(to_user_id, original_url, preview_url)
            
        elif msg_type == 'flex':
            alt_text = request.data.get('alt_text', 'You have a new message')
            flex_contents = request.data.get('flex_contents')
            if not flex_contents:
                return Response({'error': '"flex_contents" field is required for flex type.'}, status=status.HTTP_400_BAD_REQUEST)
            result = line_service.push_flex_message(to_user_id, alt_text, flex_contents)
            
        else:
            return Response({'error': f'Unsupported message type: {msg_type}'}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'error' in result:
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        return Response(result, status=status.HTTP_200_OK)
