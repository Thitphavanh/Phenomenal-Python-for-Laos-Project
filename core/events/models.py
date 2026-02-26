from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
import uuid
import qrcode
from io import BytesIO
from django.core.files import File


class EventCategory(models.Model):
    """Event categories (Workshop, Meetup, Conference, etc.)"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Tailwind/Heroicon class name")
    color = models.CharField(max_length=20, default="blue", help_text="Color theme (blue, green, purple, etc.)")

    class Meta:
        verbose_name_plural = "Event Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Event(models.Model):
    """Python for Laos Events"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    EVENT_TYPE_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('hybrid', 'Hybrid'),
    ]

    # Basic Info
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(EventCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='events')
    description = models.TextField()
    short_description = models.TextField(max_length=300, help_text="Brief description for event cards")

    # Media
    cover_image = models.ImageField(upload_to='events/covers/', blank=True, null=True)
    banner_image = models.ImageField(upload_to='events/banners/', blank=True, null=True)

    # Event Details
    event_type = models.CharField(max_length=10, choices=EVENT_TYPE_CHOICES, default='online')
    venue = models.CharField(max_length=200, blank=True, help_text="Physical location or platform name")
    venue_address = models.TextField(blank=True)
    online_link = models.URLField(blank=True, help_text="Zoom/Google Meet/etc. link")

    # Date & Time
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    registration_deadline = models.DateTimeField(null=True, blank=True)

    # Capacity
    max_attendees = models.IntegerField(default=0, help_text="0 = unlimited")
    current_attendees = models.IntegerField(default=0, editable=False)

    # Organizer
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    speakers = models.ManyToManyField(User, blank=True, related_name='speaking_events')

    # Additional Info
    requirements = models.TextField(blank=True, help_text="Prerequisites or things to bring")
    agenda = models.TextField(blank=True, help_text="Event schedule/agenda")
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")

    # Status & Settings
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    is_free = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-start_datetime']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('events:event_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    @property
    def is_upcoming(self):
        """Check if event is in the future"""
        return self.start_datetime > timezone.now()

    @property
    def is_ongoing(self):
        """Check if event is currently happening"""
        now = timezone.now()
        return self.start_datetime <= now <= self.end_datetime

    @property
    def is_past(self):
        """Check if event has ended"""
        return self.end_datetime < timezone.now()

    @property
    def is_full(self):
        """Check if event is at capacity"""
        if self.max_attendees == 0:
            return False
        return self.current_attendees >= self.max_attendees

    @property
    def registration_open(self):
        """Check if registration is still open"""
        if self.status != 'published':
            return False
        if self.is_full:
            return False
        if self.registration_deadline and self.registration_deadline < timezone.now():
            return False
        if self.is_past:
            return False
        return True

    @property
    def spots_remaining(self):
        """Calculate remaining spots"""
        if self.max_attendees == 0:
            return None
        return self.max_attendees - self.current_attendees

    def get_tags_list(self):
        """Return tags as a list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
        return []


class EventRegistration(models.Model):
    """Event registration tracking"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('payment_processing', 'Payment Processing'),
        ('registered', 'Registered'),
        ('confirmed', 'Confirmed'),
        ('attended', 'Attended'),
        ('cancelled', 'Cancelled'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_registrations')

    # Registration Details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, help_text="Special requests or notes")
    ticket_quantity = models.IntegerField(default=1)
    
    # Payment Details
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=50, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True)

    # Timestamps
    registered_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    attended_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['event', 'user']
        ordering = ['-registered_at']

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        # Update event attendee count
        if is_new:
            self.event.current_attendees = self.event.registrations.exclude(status='cancelled').count()
            self.event.save()


class BCELOnePayPayment(models.Model):
    """BCEL OnePay Payment tracking"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]

    # Unique identifiers
    payment_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    transaction_id = models.CharField(max_length=100, blank=True, help_text="BCEL OnePay transaction ID")

    # Relations
    registration = models.OneToOneField(
        EventRegistration,
        on_delete=models.CASCADE,
        related_name='payment'
    )

    # BCEL OnePay Details
    merchant_id = models.CharField(max_length=50, default='mch5f0e5f1d512c8')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='LAK')

    # Payment Info
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    qr_code_data = models.TextField(blank=True, help_text="QR code data for payment")
    qr_code_image = models.ImageField(upload_to='payments/qr_codes/', blank=True, null=True)

    # Response from BCEL OnePay
    payment_response = models.JSONField(blank=True, null=True, help_text="Response from BCEL OnePay API")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment {self.payment_id} - {self.registration.user.username}"

    def is_expired(self):
        """Check if payment QR code has expired"""
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False

    def mark_as_paid(self):
        """Mark payment as completed"""
        self.status = 'completed'
        self.paid_at = timezone.now()
        self.save()

        # Update registration status
        self.registration.status = 'confirmed'
        self.registration.confirmed_at = timezone.now()
        self.registration.transaction_id = self.transaction_id
        self.registration.save()

        # Generate ticket
        from .utils import generate_event_ticket
        generate_event_ticket(self.registration)

    def generate_qr_code(self):
        """Generate QR code for BCEL OnePay payment"""
        # BCEL OnePay uses EMVCo QR Code Standard
        # Reference: https://www.emvco.com/emv-technologies/qrcodes/

        # Format EMVCo QR String for BCEL OnePay
        qr_string = self._build_emvco_qr_string()
        self.qr_code_data = qr_string

        # Generate QR code image
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,  # Medium error correction for better scan
            box_size=10,
            border=4,
        )
        qr.add_data(qr_string)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Save to ImageField
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        file_name = f'qr_payment_{self.payment_id}.png'
        self.qr_code_image.save(file_name, File(buffer), save=False)

        self.save()

    def _build_emvco_qr_string(self):
        """
        Build EMVCo-compliant QR string for BCEL OnePay (Lao QR Standard)
        Format: Tag-Length-Value (TLV)

        Common Tags:
        00 = Payload Format Indicator (fixed: "01")
        01 = Point of Initiation Method ("11" for static, "12" for dynamic)
        29 = BCEL OnePay Merchant Account Information
        52 = Merchant Category Code
        53 = Transaction Currency (418 = LAK)
        54 = Transaction Amount
        58 = Country Code (LA)
        59 = Merchant Name
        60 = Merchant City
        62 = Additional Data
        63 = CRC (Checksum)
        """

        # Build QR components
        components = []

        # 00: Payload Format Indicator
        components.append("000201")

        # 01: Point of Initiation Method (12 = dynamic QR for single-use payment)
        components.append("010212")

        # 29: BCEL OnePay Merchant Account Information (Lao QR specific)
        # Sub-tags within tag 29:
        #   00 = Global Unique Identifier (la.bcel.onepay)
        #   01 = Merchant ID
        #   02 = Reference/Bill ID

        merchant_subfields = []

        # 00: GUI for BCEL OnePay
        gui = "la.bcel.onepay"
        merchant_subfields.append(f"00{str(len(gui)).zfill(2)}{gui}")

        # 01: Merchant ID
        merchant_subfields.append(f"01{str(len(self.merchant_id)).zfill(2)}{self.merchant_id}")

        # 02: Bill Reference (Payment ID)
        bill_ref = str(self.payment_id)[:25]
        merchant_subfields.append(f"02{str(len(bill_ref)).zfill(2)}{bill_ref}")

        merchant_info = "".join(merchant_subfields)
        merchant_info_length = str(len(merchant_info)).zfill(2)
        components.append(f"29{merchant_info_length}{merchant_info}")

        # 52: Merchant Category Code (0000 = general)
        components.append("52040000")

        # 53: Transaction Currency (418 = LAK)
        components.append("5303418")

        # 54: Transaction Amount (must be in format: XXXX.XX without leading zeros)
        amount_str = f"{float(self.amount):.2f}"
        amount_length = str(len(amount_str)).zfill(2)
        components.append(f"54{amount_length}{amount_str}")

        # 58: Country Code (LA)
        components.append("5802LA")

        # 59: Merchant Name
        merchant_name = "Python for Laos"
        name_length = str(len(merchant_name)).zfill(2)
        components.append(f"59{name_length}{merchant_name}")

        # 60: Merchant City
        city = "Vientiane"
        city_length = str(len(city)).zfill(2)
        components.append(f"60{city_length}{city}")

        # 62: Additional Data Field Template
        additional_data = []

        # 01: Bill Number
        bill_number = str(self.registration.id).zfill(6)
        additional_data.append(f"01{str(len(bill_number)).zfill(2)}{bill_number}")

        # 05: Reference Label
        ref_label = f"EVENT-{self.registration.event.id}"
        additional_data.append(f"05{str(len(ref_label)).zfill(2)}{ref_label}")

        additional_data_str = "".join(additional_data)
        additional_data_length = str(len(additional_data_str)).zfill(2)
        components.append(f"62{additional_data_length}{additional_data_str}")

        # Join all components (without CRC)
        qr_without_crc = "".join(components) + "6304"

        # Calculate CRC16-CCITT checksum
        crc = self._calculate_crc16(qr_without_crc.encode('utf-8'))

        # Complete QR string
        qr_string = qr_without_crc + crc

        return qr_string

    def _calculate_crc16(self, data):
        """
        Calculate CRC16-CCITT checksum for EMVCo QR
        Polynomial: 0x1021 (x^16 + x^12 + x^5 + 1)
        """
        crc = 0xFFFF
        for byte in data:
            crc ^= byte << 8
            for _ in range(8):
                if crc & 0x8000:
                    crc = (crc << 1) ^ 0x1021
                else:
                    crc = crc << 1
                crc &= 0xFFFF
        return f"{crc:04X}"


class EventTicket(models.Model):
    """Event tickets generated after successful payment"""
    # Unique identifiers
    ticket_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    ticket_number = models.CharField(max_length=20, unique=True, editable=False)

    # Relations
    registration = models.OneToOneField(
        EventRegistration,
        on_delete=models.CASCADE,
        related_name='ticket'
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_tickets')

    # Ticket Details
    qr_code = models.ImageField(upload_to='tickets/qr_codes/', blank=True, null=True)
    is_checked_in = models.BooleanField(default=False)
    checked_in_at = models.DateTimeField(null=True, blank=True)

    # Timestamps
    issued_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-issued_at']

    def __str__(self):
        return f"Ticket {self.ticket_number} - {self.event.title}"

    def save(self, *args, **kwargs):
        if not self.ticket_number:
            # Generate ticket number: EVENT-YYYYMMDD-XXXX
            from datetime import datetime
            date_str = datetime.now().strftime('%Y%m%d')
            count = EventTicket.objects.filter(
                event=self.event,
                issued_at__date=datetime.now().date()
            ).count() + 1
            self.ticket_number = f"{self.event.slug.upper()[:10]}-{date_str}-{count:04d}"

        super().save(*args, **kwargs)

    def generate_ticket_qr(self):
        """Generate QR code for ticket verification"""
        # QR code contains: ticket_id|ticket_number|event_id|user_id
        qr_data = f"{self.ticket_id}|{self.ticket_number}|{self.event.id}|{self.user.id}"

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer, format='PNG')
        file_name = f'ticket_qr_{self.ticket_id}.png'
        self.qr_code.save(file_name, File(buffer), save=False)

        self.save()

    def check_in(self):
        """Mark ticket as checked in"""
        if not self.is_checked_in:
            self.is_checked_in = True
            self.checked_in_at = timezone.now()
            self.save()

            # Update registration
            self.registration.status = 'attended'
            self.registration.attended_at = timezone.now()
            self.registration.save()
