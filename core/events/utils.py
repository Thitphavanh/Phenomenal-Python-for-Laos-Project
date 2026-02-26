"""
Utility functions for Events app
Including BCEL OnePay integration and ticket generation
"""
import requests
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from .models import EventTicket, BCELOnePayPayment


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
