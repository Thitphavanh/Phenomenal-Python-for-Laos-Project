from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    # Event browsing
    path('', views.EventListView.as_view(), name='event_list'),
    path('<slug:slug>/', views.EventDetailView.as_view(), name='event_detail'),

    # Registration flow
    path('<slug:slug>/register/', views.register_event, name='register_event'),
    path('<slug:slug>/cancel/', views.cancel_registration, name='cancel_registration'),

    # Payment flow (for paid events)
    path('<slug:slug>/purchase/', views.event_purchase, name='event_purchase'),
    path('<slug:slug>/payment-method/', views.event_payment_method, name='event_payment_method'),
    path('<slug:slug>/payment/<str:method>/', views.event_payment_process, name='event_payment_process'),

    # Ticket
    path('<slug:slug>/ticket/', views.event_ticket, name='event_ticket'),

    # BCEL OnePay webhook
    path('payment/webhook/', views.bcel_onepay_webhook, name='bcel_webhook'),

    # AJAX endpoints
    path('payment/status/<uuid:payment_id>/', views.check_payment_status, name='check_payment_status'),

    # Stripe endpoints
    path('payment/stripe/create-intent/<slug:slug>/', views.create_stripe_payment_intent, name='create_stripe_intent'),
    path('payment/stripe/webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('payment/stripe/status/<slug:slug>/', views.check_stripe_payment_status, name='check_stripe_status'),

    # PayPal endpoints
    path('payment/paypal/create-order/<slug:slug>/', views.create_paypal_order, name='create_paypal_order'),
    path('payment/paypal/capture-order/<slug:slug>/', views.capture_paypal_order, name='capture_paypal_order'),
    path('payment/paypal/webhook/', views.paypal_webhook, name='paypal_webhook'),

    # Ticket verification (for organizers)
    path('verify-ticket/', views.verify_ticket_view, name='verify_ticket'),
]
