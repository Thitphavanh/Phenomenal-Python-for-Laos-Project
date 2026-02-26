from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import (
    Event, EventCategory, EventRegistration,
    BCELOnePayPayment, EventTicket
)
from .utils import BCELOnePayService, verify_ticket

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
    """Step 3: Process Payment with BCEL OnePay"""
    event = get_object_or_404(Event, slug=slug)
    registration = get_object_or_404(EventRegistration, user=request.user, event=event)

    # Get or create payment
    if hasattr(registration, 'payment'):
        payment = registration.payment
    else:
        # Create BCEL OnePay payment
        payment = BCELOnePayService.create_payment(registration)

    # Check payment status (manual check)
    if request.method == 'POST' and request.POST.get('action') == 'check_status':
        # Check with BCEL OnePay API
        success = BCELOnePayService.check_payment_status(payment)

        if success and payment.status == 'completed':
            messages.success(request, "ການຈ່າຍເງິນສຳເລັດ! ປີ້ຂອງທ່ານພ້ອມແລ້ວ")
            return redirect('events:event_ticket', slug=slug)
        else:
            messages.warning(request, "ກະລຸນາລໍຖ້າ... ກຳລັງກວດສອບການຈ່າຍເງິນ")

    context = {
        'event': event,
        'registration': registration,
        'payment': payment,
        'method': method,
        'qr_data': payment.qr_code_data,
        'merchant_id': payment.merchant_id,
    }
    return render(request, 'events/payment_process.html', context)


@login_required
def event_ticket(request, slug):
    """Event Ticket / Success Page"""
    event = get_object_or_404(Event, slug=slug)
    registration = get_object_or_404(EventRegistration, user=request.user, event=event)

    # For paid events, must have completed payment
    if not event.is_free and event.price > 0:
        if registration.status != 'confirmed':
            # Check if payment exists and is completed
            if not hasattr(registration, 'payment') or registration.payment.status != 'completed':
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
