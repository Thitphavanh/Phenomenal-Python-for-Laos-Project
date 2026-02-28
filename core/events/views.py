from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from django.conf import settings

from .models import (
    Event, EventCategory, EventRegistration,
    BCELOnePayPayment, EventTicket, StripePayment, PayPalPayment
)
from .utils import BCELOnePayService, StripePaymentService, PayPalPaymentService, verify_ticket

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 9

    def get_queryset(self):
        queryset = Event.objects.filter(status='published')
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = EventCategory.objects.all()
        context['featured_events'] = Event.objects.filter(status='published', is_featured=True).order_by('-start_datetime')[:3]
        return context

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_registration'] = EventRegistration.objects.filter(
                event=self.object,
                user=self.request.user
            ).first()
        return context

@login_required
def register_event(request, slug):
    event = get_object_or_404(Event, slug=slug, status='published')
    
    # Check if already registered
    registration = EventRegistration.objects.filter(user=request.user, event=event).first()
    if registration:
        messages.info(request, "You are already registered for this event.")
        return redirect('events:event_detail', slug=slug)

    # Check if registration is open
    if not event.registration_open:
        messages.error(request, "Registration is closed for this event.")
        return redirect('events:event_detail', slug=slug)

    if request.method == 'POST':
        # Create registration
        EventRegistration.objects.create(
            event=event,
            user=request.user,
            status='registered',
            notes=request.POST.get('notes', '')
        )
        messages.success(request, f"Successfully registered for {event.title}!")
        return redirect('events:event_detail', slug=slug)
    
    return redirect('events:event_detail', slug=slug)

@login_required
def cancel_registration(request, slug):
    event = get_object_or_404(Event, slug=slug)
    registration = get_object_or_404(EventRegistration, user=request.user, event=event)

    if request.method == 'POST':
        # Use 'cancelled' status to keep history
        registration.status = 'cancelled'
        registration.cancelled_at = timezone.now()
        registration.save()

        # Force update count on event
        event.current_attendees = event.registrations.exclude(status='cancelled').count()
        event.save()

        messages.success(request, "ຍົກເລີກການລົງທະບຽນສຳເລັດແລ້ວ")
        return redirect('events:event_detail', slug=slug)

    # If not POST, redirect back to event detail
    return redirect('events:event_detail', slug=slug)
        
@login_required
def event_purchase(request, slug):
    """Step 1: Confirm purchase details"""
    event = get_object_or_404(Event, slug=slug, status='published')

    # Check if existing registration exists (pending or otherwise)
    registration = EventRegistration.objects.filter(user=request.user, event=event).first()

    # If already fully registered/confirmed, redirect to detail
    if registration and registration.status in ['registered', 'confirmed', 'attended']:
        messages.info(request, "You are already registered for this event.")
        return redirect('events:event_detail', slug=slug)

    if request.method == 'POST':
        ticket_quantity = int(request.POST.get('ticket_quantity', 1))
        notes = request.POST.get('notes', '')

        # Calculate total
        total_amount = event.price * ticket_quantity

        if not registration:
            registration = EventRegistration.objects.create(
                event=event,
                user=request.user,
                status='pending' if not event.is_free else 'registered',
                ticket_quantity=ticket_quantity,
                total_amount=total_amount,
                notes=notes
            )
        else:
            # Update existing pending registration
            registration.ticket_quantity = ticket_quantity
            registration.total_amount = total_amount
            registration.notes = notes
            registration.status = 'pending' if not event.is_free else 'registered'
            registration.save()

        # For FREE events, skip payment and go directly to success
        if event.is_free:
            # Generate ticket immediately for free events
            from .utils import generate_event_ticket
            generate_event_ticket(registration)

            messages.success(request, f"ລົງທະບຽນສຳເລັດ! ປີ້ຂອງທ່ານພ້ອມແລ້ວ")
            return redirect('events:event_ticket', slug=slug)

        # For paid events, proceed to payment
        return redirect('events:event_payment_method', slug=slug)

    context = {
        'event': event,
        'registration': registration
    }
    return render(request, 'events/event_purchase.html', context)


@login_required
def event_payment_method(request, slug):
    """Step 2: Select Payment Method"""
    event = get_object_or_404(Event, slug=slug)
    registration = get_object_or_404(EventRegistration, user=request.user, event=event)
    
    if registration.status in ['registered', 'confirmed']:
        return redirect('events:event_detail', slug=slug)
        
    if request.method == 'POST':
        method = request.POST.get('payment_method')
        if method:
            registration.payment_method = method
            registration.status = 'payment_processing'
            registration.save()
            return redirect('events:event_payment_process', slug=slug, method=method)
        else:
            messages.error(request, "Please select a payment method")
            
    return render(request, 'events/payment_method.html', {'event': event, 'registration': registration})


@login_required
def event_payment_process(request, slug, method):
    """Step 3: Process Payment — dispatches by payment method"""
    event = get_object_or_404(Event, slug=slug)
    registration = get_object_or_404(EventRegistration, user=request.user, event=event)

    context = {
        'event': event,
        'registration': registration,
        'method': method,
    }

    if method == 'STRIPE':
        if not getattr(settings, 'STRIPE_SECRET_KEY', None) or not getattr(settings, 'STRIPE_PUBLISHABLE_KEY', None):
            messages.error(request, "ລະບົບຍັງບໍ່ທັນໄດ້ຕັ້ງຄ່າ Stripe API Keys. ກະລຸນາເພີ່ມ STRIPE_SECRET_KEY ໃນ .env")
            return redirect('events:event_payment_method', slug=slug)

        try:
            payment = StripePaymentService.create_payment_intent(registration, pm_type='card')
            context['stripe_client_secret'] = payment.client_secret
            context['stripe_publishable_key'] = settings.STRIPE_PUBLISHABLE_KEY
            context['amount_usd'] = payment.amount_usd
        except Exception as e:
            messages.error(request, f"Stripe error: {e}")
            return redirect('events:event_payment_method', slug=slug)
        return render(request, 'events/payment_stripe.html', context)

    elif method == 'PROMPTPAY':
        if not getattr(settings, 'STRIPE_SECRET_KEY', None) or not getattr(settings, 'STRIPE_PUBLISHABLE_KEY', None):
            messages.error(request, "ລະບົບຍັງບໍ່ທັນໄດ້ຕັ້ງຄ່າ Stripe API Keys. ກະລຸນາເພີ່ມ STRIPE_SECRET_KEY ໃນ .env")
            return redirect('events:event_payment_method', slug=slug)

        try:
            payment = StripePaymentService.create_payment_intent(registration, pm_type='promptpay')
            context['stripe_client_secret'] = payment.client_secret
            context['stripe_publishable_key'] = settings.STRIPE_PUBLISHABLE_KEY
            context['amount_thb'] = payment.amount_usd
            
            intent = getattr(payment, 'intent_obj', None)
            if intent and intent.next_action and intent.next_action.promptpay_display_qr_code:
                context['promptpay_qr_url'] = intent.next_action.promptpay_display_qr_code.image_url_svg
        except Exception as e:
            messages.error(request, f"Stripe PromptPay error: {e}")
            return redirect('events:event_payment_method', slug=slug)
        return render(request, 'events/payment_promptpay.html', context)

    elif method == 'PAYPAL':
        if not getattr(settings, 'PAYPAL_CLIENT_ID', None) or not getattr(settings, 'PAYPAL_CLIENT_SECRET', None):
            messages.error(request, "ລະບົບຍັງບໍ່ທັນໄດ້ຕັ້ງຄ່າ PayPal API Keys. ກະລຸນາເພີ່ມ PAYPAL_CLIENT_ID ແລະ PAYPAL_CLIENT_SECRET ໃນ .env")
            return redirect('events:event_payment_method', slug=slug)

        context['paypal_client_id'] = settings.PAYPAL_CLIENT_ID
        rate = getattr(settings, 'LAK_TO_USD_RATE', 21000)
        context['amount_usd'] = round(float(registration.total_amount) / float(rate), 2)
        return render(request, 'events/payment_paypal.html', context)

    else:
        # Default: BCEL OnePay
        if hasattr(registration, 'payment'):
            payment = registration.payment
        else:
            payment = BCELOnePayService.create_payment(registration)

        if request.method == 'POST' and request.POST.get('action') == 'check_status':
            success = BCELOnePayService.check_payment_status(payment)
            if success and payment.status == 'completed':
                messages.success(request, "ການຈ່າຍເງິນສຳເລັດ! ປີ້ຂອງທ່ານພ້ອມແລ້ວ")
                return redirect('events:event_ticket', slug=slug)
            else:
                messages.warning(request, "ກະລຸນາລໍຖ້າ... ກຳລັງກວດສອບການຈ່າຍເງິນ")

        context.update({
            'payment': payment,
            'qr_data': payment.qr_code_data,
            'merchant_id': payment.merchant_id,
        })
        return render(request, 'events/payment_process.html', context)


def _has_completed_payment(registration):
    """Return True if any payment type for this registration is completed."""
    if hasattr(registration, 'payment') and registration.payment.status == 'completed':
        return True
    if hasattr(registration, 'stripe_payment') and registration.stripe_payment.status == 'completed':
        return True
    if hasattr(registration, 'paypal_payment') and registration.paypal_payment.status == 'completed':
        return True
    return False


@login_required
def event_ticket(request, slug):
    """Event Ticket / Success Page"""
    event = get_object_or_404(Event, slug=slug)
    registration = get_object_or_404(EventRegistration, user=request.user, event=event)

    # For paid events, must have completed payment
    if not event.is_free and event.price > 0:
        if registration.status != 'confirmed':
            if not _has_completed_payment(registration):
                messages.error(request, "ກະລຸນາຊຳລະເງິນກ່ອນເບິ່ງປີ້")
                return redirect('events:event_payment_method', slug=slug)

    # Check if ticket exists, if not create one (for free events)
    if not hasattr(registration, 'ticket'):
        if event.is_free:
            # Auto-generate ticket for free events
            from .utils import generate_event_ticket
            generate_event_ticket(registration)
        else:
            messages.error(request, "ຍັງບໍ່ມີປີ້ ກະລຸນາຊຳລະເງິນກ່ອນ")
            return redirect('events:event_detail', slug=slug)

    ticket = registration.ticket

    context = {
        'event': event,
        'registration': registration,
        'ticket': ticket,
    }
    return render(request, 'events/event_ticket.html', context)


@csrf_exempt
def bcel_onepay_webhook(request):
    """
    Webhook endpoint for BCEL OnePay payment notifications
    BCEL OnePay will call this URL when payment is completed
    """
    if request.method == 'POST':
        try:
            # Parse webhook data
            data = json.loads(request.body)

            # Process webhook
            success = BCELOnePayService.process_webhook(data)

            if success:
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'failed'}, status=400)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'method not allowed'}, status=405)


@login_required
def check_payment_status(request, payment_id):
    """
    AJAX endpoint to check payment status
    Called from frontend to poll payment status
    """
    try:
        payment = get_object_or_404(BCELOnePayPayment, payment_id=payment_id)

        # Check with BCEL OnePay
        BCELOnePayService.check_payment_status(payment)

        return JsonResponse({
            'status': payment.status,
            'paid': payment.status == 'completed',
            'ticket_url': None if payment.status != 'completed' else f'/events/{payment.registration.event.slug}/ticket/'
        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@login_required
def verify_ticket_view(request):
    """
    Ticket verification view (for event organizers)
    Scan QR code to verify ticket at event entrance
    """
    if request.method == 'POST':
        ticket_data = request.POST.get('ticket_data')

        valid, ticket, message = verify_ticket(ticket_data)

        if valid and ticket:
            # Check in the ticket
            ticket.check_in()
            return JsonResponse({
                'valid': True,
                'message': 'ປີ້ຖືກຕ້ອງ! ເຂົ້າງານໄດ້',
                'ticket': {
                    'number': ticket.ticket_number,
                    'user': ticket.user.get_full_name() or ticket.user.username,
                    'event': ticket.event.title,
                }
            })
        else:
            return JsonResponse({
                'valid': False,
                'message': message
            })

    return render(request, 'events/verify_ticket.html')


# ──────────────────────────────────────────────
# Stripe views
# ──────────────────────────────────────────────

@login_required
def create_stripe_payment_intent(request, slug):
    """Create / refresh a Stripe PaymentIntent for the event."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    event = get_object_or_404(Event, slug=slug)
    registration = get_object_or_404(EventRegistration, user=request.user, event=event)
    try:
        payment = StripePaymentService.create_payment_intent(registration)
        return JsonResponse({
            'clientSecret': payment.client_secret,
            'amountUsd': float(payment.amount_usd),
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def check_stripe_payment_status(request, slug):
    """Poll Stripe payment status — frontend calls this after confirmCardPayment."""
    event = get_object_or_404(Event, slug=slug)
    registration = get_object_or_404(EventRegistration, user=request.user, event=event)
    try:
        stripe_payment = registration.stripe_payment
    except StripePayment.DoesNotExist:
        return JsonResponse({'paid': False, 'status': 'not_found'})

    # If already marked complete, return early
    if stripe_payment.status == 'completed':
        return JsonResponse({
            'paid': True,
            'status': 'completed',
            'ticket_url': f'/events/{slug}/ticket/',
        })

    # Verify with Stripe
    try:
        success, intent = StripePaymentService.confirm_payment(stripe_payment.payment_intent_id)
        if success and stripe_payment.status != 'completed':
            stripe_payment.payment_response = dict(intent)
            stripe_payment.mark_as_paid()
        return JsonResponse({
            'paid': stripe_payment.status == 'completed',
            'status': stripe_payment.status,
            'ticket_url': f'/events/{slug}/ticket/' if stripe_payment.status == 'completed' else None,
        })
    except Exception as e:
        return JsonResponse({'paid': False, 'status': 'error', 'error': str(e)}, status=500)


@csrf_exempt
def stripe_webhook(request):
    """Stripe webhook endpoint — receives payment_intent.succeeded etc."""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
    try:
        StripePaymentService.process_webhook(payload, sig_header)
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# ──────────────────────────────────────────────
# PayPal views
# ──────────────────────────────────────────────

@login_required
def create_paypal_order(request, slug):
    """Create a PayPal order — called from PayPal JS SDK onCreateOrder."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    event = get_object_or_404(Event, slug=slug)
    registration = get_object_or_404(EventRegistration, user=request.user, event=event)
    try:
        payment = PayPalPaymentService.create_order(registration)
        return JsonResponse({'id': payment.order_id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def capture_paypal_order(request, slug):
    """Capture an approved PayPal order — called from JS onApprove."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    event = get_object_or_404(Event, slug=slug)
    registration = get_object_or_404(EventRegistration, user=request.user, event=event)

    try:
        data = json.loads(request.body)
        order_id = data.get('orderID', '')
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    try:
        success, capture_id, capture_data = PayPalPaymentService.capture_order(order_id)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

    if success:
        try:
            pp = registration.paypal_payment
        except PayPalPayment.DoesNotExist:
            pp = PayPalPayment.objects.create(
                registration=registration,
                order_id=order_id,
            )
        pp.capture_id = capture_id
        pp.payment_response = capture_data
        pp.amount_usd = PayPalPaymentService._lak_to_usd(registration.total_amount)
        pp.save()
        pp.mark_as_paid()
        return JsonResponse({'success': True, 'ticket_url': f'/events/{slug}/ticket/'})

    return JsonResponse({'success': False, 'error': 'Capture failed'}, status=400)


@csrf_exempt
def paypal_webhook(request):
    """PayPal webhook endpoint."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    try:
        data = json.loads(request.body)
        event_type = data.get('event_type', '')
        if event_type == 'PAYMENT.CAPTURE.COMPLETED':
            resource = data.get('resource', {})
            custom_id = resource.get('custom_id') or (
                resource.get('purchase_units', [{}])[0].get('custom_id', '')
                if resource.get('purchase_units') else ''
            )
            capture_id = resource.get('id', '')
            if custom_id:
                try:
                    registration = EventRegistration.objects.get(id=custom_id)
                    pp, _ = PayPalPayment.objects.get_or_create(registration=registration)
                    if pp.status != 'completed':
                        pp.capture_id = capture_id
                        pp.payment_response = data
                        pp.mark_as_paid()
                except EventRegistration.DoesNotExist:
                    pass
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
