"""
Utility functions for Events app
Including BCEL OnePay, Stripe, and PayPal integrations and ticket generation
"""
import requests
import stripe
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from .models import EventTicket, BCELOnePayPayment, StripePayment, PayPalPayment


class BCELOnePayService:
    """
    Service class for BCEL OnePay integration
    """
    MERCHANT_ID = 'mch5f0e5f1d512c8'

    # BCEL OnePay API endpoints (ປັບແກ້ໃຫ້ຕົງກັບ API ຈິງ)
    API_BASE_URL = getattr(settings, 'BCEL_ONEPAY_API_URL', 'https://api.bcel.com.la/onepay')
    API_KEY = getattr(settings, 'BCEL_ONEPAY_API_KEY', '')

    @classmethod
    def create_payment(cls, registration):
        """
        Create BCEL OnePay payment for event registration

        Args:
            registration: EventRegistration instance

        Returns:
            BCELOnePayPayment instance
        """
        # Calculate payment amount
        amount = registration.total_amount

        # Create payment record
        payment = BCELOnePayPayment.objects.create(
            registration=registration,
            merchant_id=cls.MERCHANT_ID,
            amount=amount,
            currency='LAK',
            status='pending',
            expires_at=timezone.now() + timedelta(minutes=30)  # Payment QR expires in 30 minutes
        )

        # Generate QR code
        payment.generate_qr_code()

        # Optional: Call BCEL OnePay API to register payment
        # cls._register_payment_with_api(payment)

        return payment

    @classmethod
    def _register_payment_with_api(cls, payment):
        """
        Register payment with BCEL OnePay API
        (ຕ້ອງປັບແກ້ໃຫ້ຕົງກັບ API documentation ຂອງ BCEL OnePay)
        """
        try:
            payload = {
                'merchant_id': payment.merchant_id,
                'payment_id': str(payment.payment_id),
                'amount': float(payment.amount),
                'currency': payment.currency,
                'callback_url': f"{settings.SITE_URL}/events/payment/callback/",
            }

            headers = {
                'Authorization': f'Bearer {cls.API_KEY}',
                'Content-Type': 'application/json'
            }

            response = requests.post(
                f'{cls.API_BASE_URL}/create-payment',
                json=payload,
                headers=headers,
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                payment.payment_response = data
                payment.save()
                return True

            return False

        except Exception as e:
            print(f"Error registering payment with BCEL OnePay: {e}")
            return False

    @classmethod
    def check_payment_status(cls, payment):
        """
        Check payment status from BCEL OnePay
        (ຕ້ອງປັບແກ້ໃຫ້ຕົງກັບ API documentation)
        """
        try:
            headers = {
                'Authorization': f'Bearer {cls.API_KEY}',
                'Content-Type': 'application/json'
            }

            response = requests.get(
                f'{cls.API_BASE_URL}/payment-status/{payment.payment_id}',
                headers=headers,
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                status = data.get('status')

                if status == 'completed':
                    payment.transaction_id = data.get('transaction_id', '')
                    payment.mark_as_paid()
                    return True

            return False

        except Exception as e:
            print(f"Error checking payment status: {e}")
            return False

    @classmethod
    def process_webhook(cls, webhook_data):
        """
        Process webhook callback from BCEL OnePay
        Called when payment is completed
        """
        try:
            payment_id = webhook_data.get('payment_id')
            status = webhook_data.get('status')
            transaction_id = webhook_data.get('transaction_id')

            payment = BCELOnePayPayment.objects.get(payment_id=payment_id)

            if status == 'completed':
                payment.transaction_id = transaction_id
                payment.mark_as_paid()
                return True

            elif status == 'failed':
                payment.status = 'failed'
                payment.save()

                # Update registration
                payment.registration.status = 'cancelled'
                payment.registration.save()

            return False

        except BCELOnePayPayment.DoesNotExist:
            print(f"Payment not found: {payment_id}")
            return False
        except Exception as e:
            print(f"Error processing webhook: {e}")
            return False


class StripePaymentService:
    """Service class for Stripe credit/debit card payments"""

    @classmethod
    def _lak_to_currency_cents(cls, lak_amount, currency='usd'):
        """Convert LAK amount to currency cents for Stripe"""
        if currency == 'usd':
            rate = getattr(settings, 'LAK_TO_USD_RATE', 21000)
        elif currency == 'thb':
            rate = getattr(settings, 'LAK_TO_THB_RATE', 650)
        else:
            raise ValueError(f"Unsupported currency: {currency}")

        amount = float(lak_amount) / float(rate)
        return int(amount * 100), round(amount, 2)

    @classmethod
    def create_payment_intent(cls, registration, pm_type='card'):
        """Create Stripe PaymentIntent and StripePayment record"""
        currency = 'thb' if pm_type == 'promptpay' else 'usd'
        amount_cents, amount_converted = cls._lak_to_currency_cents(registration.total_amount, currency)

        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        intent_kwargs = {
            'amount': amount_cents,
            'currency': currency,
            'payment_method_types': [pm_type],
            'metadata': {
                'registration_id': registration.id,
                'event': registration.event.title,
            }
        }
        
        if pm_type == 'promptpay':
            intent_kwargs.update({
                'payment_method_data': {
                    'type': 'promptpay',
                    'billing_details': {
                        'email': registration.user.email or 'no-reply@pythonforlaos.com'
                    }
                },
                'confirm': True,
            })
            
        intent = stripe.PaymentIntent.create(**intent_kwargs)

        payment, created = StripePayment.objects.get_or_create(
            registration=registration,
            defaults={
                'payment_intent_id': intent.id,
                'client_secret': intent.client_secret,
                'amount_usd': amount_converted,
                'currency': currency,
            }
        )
        if not created:
            payment.payment_intent_id = intent.id
            payment.client_secret = intent.client_secret
            payment.amount_usd = amount_converted
            payment.currency = currency
            # Reset status since we are generating a new payment intent for this registration
            payment.status = 'pending'
            payment.payment_response = None
            payment.paid_at = None
            payment.save()

        payment.intent_obj = intent
        return payment

    @classmethod
    def confirm_payment(cls, payment_intent_id):
        """Retrieve PaymentIntent from Stripe and verify success"""
        stripe.api_key = settings.STRIPE_SECRET_KEY
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        return intent.status == 'succeeded', intent

    @classmethod
    def process_webhook(cls, payload, sig_header):
        """Handle Stripe webhook events"""
        stripe.api_key = settings.STRIPE_SECRET_KEY
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
        if event.type == 'payment_intent.succeeded':
            pi = event.data.object
            try:
                payment = StripePayment.objects.get(payment_intent_id=pi.id)
                if payment.status != 'completed':
                    payment.payment_response = dict(pi)
                    payment.mark_as_paid()
            except StripePayment.DoesNotExist:
                pass
        elif event.type == 'payment_intent.payment_failed':
            pi = event.data.object
            try:
                payment = StripePayment.objects.get(payment_intent_id=pi.id)
                payment.status = 'failed'
                payment.save()
            except StripePayment.DoesNotExist:
                pass
        return event


class PayPalPaymentService:
    """Service class for PayPal payments via REST API"""

    SANDBOX_BASE = 'https://api-m.sandbox.paypal.com'
    LIVE_BASE = 'https://api-m.paypal.com'

    @classmethod
    def _base_url(cls):
        mode = getattr(settings, 'PAYPAL_MODE', 'sandbox')
        return cls.SANDBOX_BASE if mode == 'sandbox' else cls.LIVE_BASE

    @classmethod
    def _get_access_token(cls):
        """Obtain PayPal OAuth2 access token"""
        url = f'{cls._base_url()}/v1/oauth2/token'
        response = requests.post(
            url,
            headers={'Accept': 'application/json'},
            data={'grant_type': 'client_credentials'},
            auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET),
            timeout=10,
        )
        response.raise_for_status()
        return response.json()['access_token']

    @classmethod
    def _lak_to_usd(cls, lak_amount):
        rate = getattr(settings, 'LAK_TO_USD_RATE', 21000)
        return round(float(lak_amount) / float(rate), 2)

    @classmethod
    def create_order(cls, registration):
        """Create a PayPal order and return PayPalPayment instance"""
        amount_usd = cls._lak_to_usd(registration.total_amount)
        token = cls._get_access_token()

        url = f'{cls._base_url()}/v2/checkout/orders'
        payload = {
            'intent': 'CAPTURE',
            'purchase_units': [{
                'amount': {
                    'currency_code': 'USD',
                    'value': f'{amount_usd:.2f}',
                },
                'description': registration.event.title,
                'custom_id': str(registration.id),
            }],
        }
        response = requests.post(
            url,
            json=payload,
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json',
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        order_id = data['id']

        payment, created = PayPalPayment.objects.get_or_create(
            registration=registration,
            defaults={
                'order_id': order_id,
                'amount_usd': amount_usd,
                'payment_response': data,
            }
        )
        if not created:
            payment.order_id = order_id
            payment.amount_usd = amount_usd
            payment.payment_response = data
            payment.save()

        return payment

    @classmethod
    def capture_order(cls, order_id):
        """Capture an approved PayPal order"""
        token = cls._get_access_token()
        url = f'{cls._base_url()}/v2/checkout/orders/{order_id}/capture'
        response = requests.post(
            url,
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json',
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        status = data.get('status')
        success = status == 'COMPLETED'

        capture_id = ''
        if success:
            try:
                capture_id = data['purchase_units'][0]['payments']['captures'][0]['id']
            except (KeyError, IndexError):
                pass

        return success, capture_id, data


def generate_event_ticket(registration):
    """
    Generate event ticket after successful payment

    Args:
        registration: EventRegistration instance

    Returns:
        EventTicket instance
    """
    # Check if ticket already exists
    if hasattr(registration, 'ticket'):
        return registration.ticket

    # Create ticket
    ticket = EventTicket.objects.create(
        registration=registration,
        event=registration.event,
        user=registration.user
    )

    # Generate QR code for ticket
    ticket.generate_ticket_qr()

    # Optional: Send ticket via email
    # send_ticket_email(ticket)

    return ticket


def send_ticket_email(ticket):
    """
    Send ticket to user via email
    (ຕ້ອງຕິດຕັ້ງ email configuration)
    """
    from django.core.mail import EmailMessage
    from django.template.loader import render_to_string

    subject = f'ປີ້ເຂົ້າງານ - {ticket.event.title}'

    # Render email template
    html_content = render_to_string('events/emails/ticket_email.html', {
        'ticket': ticket,
        'event': ticket.event,
        'user': ticket.user
    })

    email = EmailMessage(
        subject=subject,
        body=html_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[ticket.user.email]
    )
    email.content_subtype = 'html'

    # Attach QR code
    if ticket.qr_code:
        email.attach_file(ticket.qr_code.path)

    email.send()


def verify_ticket(ticket_data):
    """
    Verify ticket QR code at event check-in

    Args:
        ticket_data: String from QR code scan (format: ticket_id|ticket_number|event_id|user_id)

    Returns:
        tuple: (valid, ticket, message)
    """
    try:
        parts = ticket_data.split('|')
        if len(parts) != 4:
            return (False, None, "Invalid QR code format")

        ticket_id, ticket_number, event_id, user_id = parts

        # Find ticket
        ticket = EventTicket.objects.get(
            ticket_id=ticket_id,
            ticket_number=ticket_number,
            event_id=event_id,
            user_id=user_id
        )

        # Check if already checked in
        if ticket.is_checked_in:
            return (False, ticket, "Ticket already checked in")

        # Check if event has started
        if ticket.event.start_datetime > timezone.now():
            return (False, ticket, "Event has not started yet")

        return (True, ticket, "Valid ticket")

    except EventTicket.DoesNotExist:
        return (False, None, "Ticket not found")
    except Exception as e:
        return (False, None, f"Error: {str(e)}")
