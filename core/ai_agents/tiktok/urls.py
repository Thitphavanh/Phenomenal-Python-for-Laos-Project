from django.urls import path
from . import views

app_name = 'tiktok'

urlpatterns = [
    path('webhook/', views.tiktok_webhook, name='webhook'),
    path('shop-webhook/', views.tiktok_shop_webhook, name='shop_webhook'),
    path('force-check/', views.force_check_comments, name='force_check'),
    path('post-video/', views.post_tiktok_video, name='post_video'),
    path('dashboard/', views.tiktok_dashboard, name='dashboard'),
]
