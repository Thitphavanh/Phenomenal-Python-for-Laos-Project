"""
URL Configuration for AI Agents
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'ai_agents'

# REST Framework Router
router = DefaultRouter()
router.register(r'analytics', views.CourseAnalyticsViewSet, basename='analytics')
router.register(r'payment-slips', views.PaymentSlipAnalysisViewSet, basename='payment-slips')
router.register(r'recommendations', views.CourseRecommendationViewSet, basename='recommendations')

urlpatterns = [
    # UI Pages
    path('chatbot/', views.chatbot_page, name='chatbot'),
    path('dashboard/', views.analytics_dashboard, name='dashboard'),
    
    # API Endpoints
    path('api/chat/', views.ChatAPIView.as_view(), name='chat-api'),
    # WhatsApp Webhook
    path('api/whatsapp/webhook/', views.WhatsAppWebhookView.as_view(), name='whatsapp-webhook'),
    
    # LINE Integrations
    path('line/login/', views.line_login_page, name='line-login'),
    path('api/line/webhook/', views.LineWebhookView.as_view(), name='line-webhook'),
    path('api/line/push/', views.LinePushMessageView.as_view(), name='line-push'),

    # REST Framework Router URLs
    path('api/', include(router.urls)),
]
