from django.contrib import admin
from .models import (
    ChatConversation,
    ChatMessage,
    CourseAnalytics,
    PaymentSlipAnalysis,
    CourseRecommendation,
    VectorDocument
)


@admin.register(ChatConversation)
class ChatConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_id', 'started_at', 'last_message_at', 'is_active')
    list_filter = ('is_active', 'started_at')
    search_fields = ('session_id', 'user__username')
    date_hierarchy = 'started_at'
    readonly_fields = ('session_id', 'started_at', 'last_message_at')


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'role', 'content_preview', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('content', 'conversation__session_id')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)

    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content'


@admin.register(CourseAnalytics)
class CourseAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'student_engagement_score', 'completion_rate_prediction', 'generated_at', 'is_current')
    list_filter = ('is_current', 'generated_at')
    search_fields = ('course__title', 'recommendations')
    date_hierarchy = 'generated_at'
    readonly_fields = ('generated_at',)

    fieldsets = (
        ('Course Information', {
            'fields': ('course', 'is_current')
        }),
        ('Analytics Metrics', {
            'fields': ('student_engagement_score', 'completion_rate_prediction', 'enrollment_prediction', 'performance_insights')
        }),
        ('AI Recommendations', {
            'fields': ('recommendations', 'suggested_improvements')
        }),
        ('Metadata', {
            'fields': ('generated_at',)
        }),
    )


@admin.register(PaymentSlipAnalysis)
class PaymentSlipAnalysisAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'transaction_id', 'status', 'confidence_score', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('transaction_id', 'sender_name', 'user__username')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'processed_at')

    fieldsets = (
        ('Image', {
            'fields': ('image',)
        }),
        ('Extracted Information', {
            'fields': ('amount', 'transaction_id', 'payment_date', 'sender_name', 'extracted_data')
        }),
        ('AI Analysis', {
            'fields': ('status', 'confidence_score', 'notes')
        }),
        ('Relations', {
            'fields': ('user', 'event_registration')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'processed_at')
        }),
    )


@admin.register(CourseRecommendation)
class CourseRecommendationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recommended_course', 'relevance_score', 'was_viewed', 'was_enrolled', 'generated_at')
    list_filter = ('is_active', 'was_viewed', 'was_enrolled', 'generated_at')
    search_fields = ('user__username', 'recommended_course__title', 'reason')
    date_hierarchy = 'generated_at'
    readonly_fields = ('generated_at', 'viewed_at')

    fieldsets = (
        ('Recommendation', {
            'fields': ('user', 'recommended_course', 'is_active')
        }),
        ('Details', {
            'fields': ('relevance_score', 'reason', 'based_on')
        }),
        ('User Interaction', {
            'fields': ('was_viewed', 'was_enrolled', 'viewed_at')
        }),
        ('Metadata', {
            'fields': ('generated_at',)
        }),
    )


@admin.register(VectorDocument)
class VectorDocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'document_type', 'document_id', 'vector_id', 'collection_name', 'created_at', 'updated_at')
    list_filter = ('document_type', 'collection_name', 'created_at')
    search_fields = ('vector_id', 'content')
    date_hierarchy = 'updated_at'
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Document Info', {
            'fields': ('document_type', 'document_id', 'content')
        }),
        ('Vector DB Info', {
            'fields': ('vector_id', 'collection_name', 'metadata')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
