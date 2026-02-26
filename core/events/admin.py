from django.contrib import admin
from django.utils.html import format_html
from .models import (
    EventCategory, Event, EventRegistration,
    BCELOnePayPayment, EventTicket
)


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color', 'icon')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    list_filter = ('color',)

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description')
        }),
        ('Display', {
            'fields': ('icon', 'color')
        }),
    )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'category', 'status', 'event_type', 'start_datetime',
        'current_attendees', 'max_attendees', 'is_free', 'price', 'is_featured'
    )
    list_filter = ('status', 'event_type', 'is_featured', 'is_free', 'category', 'start_datetime')
    search_fields = ('title', 'description', 'venue')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'start_datetime'
    autocomplete_fields = ['organizer', 'speakers']
    list_editable = ['status', 'is_featured']
    readonly_fields = ('current_attendees', 'published_at')

    fieldsets = (
        ('ຂໍ້ມູນພື້ນຖານ', {
            'fields': ('title', 'slug', 'category', 'short_description', 'description')
        }),
        ('ຮູບພາບ', {
            'fields': ('cover_image', 'banner_image')
        }),
        ('ລາຍລະອຽດງານ', {
            'fields': (
                'event_type', 'venue', 'venue_address', 'online_link'
            )
        }),
        ('ວັນແລະເວລາ', {
            'fields': (
                'start_datetime', 'end_datetime', 'registration_deadline'
            )
        }),
        ('ຈຳນວນຜູ້ເຂົ້າຮ່ວມ', {
            'fields': ('max_attendees', 'current_attendees')
        }),
        ('ຜູ້ຈັດງານ', {
            'fields': ('organizer', 'speakers')
        }),
        ('ຂໍ້ມູນເພີ່ມເຕີມ', {
            'fields': ('requirements', 'agenda', 'tags'),
            'classes': ('collapse',)
        }),
        ('ລາຄາ', {
            'fields': ('is_free', 'price')
        }),
        ('ສະຖານະ', {
            'fields': ('status', 'is_featured', 'published_at')
        }),
    )


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = (
        'event', 'user', 'status', 'ticket_quantity', 'total_amount',
        'payment_status', 'has_ticket', 'registered_at'
    )
    list_filter = ('status', 'registered_at', 'event')
    search_fields = ('user__username', 'user__email', 'event__title', 'transaction_id')
    autocomplete_fields = ['user', 'event']
    readonly_fields = ('registered_at', 'confirmed_at', 'attended_at', 'cancelled_at')
    list_per_page = 50

    fieldsets = (
        ('ຂໍ້ມູນການລົງທະບຽນ', {
            'fields': ('event', 'user', 'status', 'ticket_quantity', 'notes')
        }),
        ('ການຈ່າຍເງິນ', {
            'fields': ('total_amount', 'payment_method', 'transaction_id')
        }),
        ('ເວລາ', {
            'fields': ('registered_at', 'confirmed_at', 'attended_at', 'cancelled_at')
        }),
    )

    def payment_status(self, obj):
        """Show payment status"""
        if hasattr(obj, 'payment'):
            payment = obj.payment
            colors = {
                'pending': 'orange',
                'processing': 'blue',
                'completed': 'green',
                'failed': 'red',
                'cancelled': 'gray'
            }
            color = colors.get(payment.status, 'gray')
            return format_html(
                '<span style="color: {};">{}</span>',
                color,
                payment.get_status_display()
            )
        return format_html('<span style="color: gray;">No payment</span>')
    payment_status.short_description = 'Payment Status'

    def has_ticket(self, obj):
        """Show if ticket has been issued"""
        if hasattr(obj, 'ticket'):
            return format_html('<span style="color: green;">✓</span>')
        return format_html('<span style="color: red;">✗</span>')
    has_ticket.short_description = 'Ticket'


@admin.register(BCELOnePayPayment)
class BCELOnePayPaymentAdmin(admin.ModelAdmin):
    list_display = (
        'payment_id', 'get_event', 'get_user', 'amount', 'currency',
        'status', 'created_at', 'paid_at', 'is_expired'
    )
    list_filter = ('status', 'currency', 'created_at', 'paid_at')
    search_fields = (
        'payment_id', 'transaction_id',
        'registration__user__username',
        'registration__event__title'
    )
    readonly_fields = (
        'payment_id', 'qr_code_data', 'qr_code_image',
        'created_at', 'paid_at', 'payment_response'
    )
    list_per_page = 50

    fieldsets = (
        ('ຂໍ້ມູນການຈ່າຍເງິນ', {
            'fields': ('payment_id', 'transaction_id', 'registration')
        }),
        ('BCEL OnePay', {
            'fields': ('merchant_id', 'amount', 'currency', 'status')
        }),
        ('QR Code', {
            'fields': ('qr_code_data', 'qr_code_image')
        }),
        ('Response', {
            'fields': ('payment_response',),
            'classes': ('collapse',)
        }),
        ('ເວລາ', {
            'fields': ('created_at', 'paid_at', 'expires_at')
        }),
    )

    def get_event(self, obj):
        """Get event name"""
        return obj.registration.event.title
    get_event.short_description = 'Event'

    def get_user(self, obj):
        """Get user"""
        return obj.registration.user.username
    get_user.short_description = 'User'

    def is_expired(self, obj):
        """Show if payment has expired"""
        if obj.is_expired():
            return format_html('<span style="color: red;">Expired</span>')
        return format_html('<span style="color: green;">Active</span>')
    is_expired.short_description = 'Status'


@admin.register(EventTicket)
class EventTicketAdmin(admin.ModelAdmin):
    list_display = (
        'ticket_number', 'event', 'user', 'is_checked_in',
        'checked_in_at', 'issued_at'
    )
    list_filter = ('is_checked_in', 'event', 'issued_at', 'checked_in_at')
    search_fields = (
        'ticket_number', 'ticket_id',
        'user__username', 'user__email',
        'event__title'
    )
    readonly_fields = (
        'ticket_id', 'ticket_number', 'qr_code',
        'issued_at', 'checked_in_at'
    )
    autocomplete_fields = ['event', 'user']
    list_per_page = 50

    fieldsets = (
        ('ຂໍ້ມູນປີ້', {
            'fields': ('ticket_id', 'ticket_number', 'registration', 'event', 'user')
        }),
        ('QR Code', {
            'fields': ('qr_code',)
        }),
        ('Check-in', {
            'fields': ('is_checked_in', 'checked_in_at', 'issued_at')
        }),
    )

    actions = ['check_in_tickets']

    def check_in_tickets(self, request, queryset):
        """Bulk check-in tickets"""
        count = 0
        for ticket in queryset:
            if not ticket.is_checked_in:
                ticket.check_in()
                count += 1
        self.message_user(request, f'{count} tickets checked in successfully.')
    check_in_tickets.short_description = 'Check in selected tickets'
