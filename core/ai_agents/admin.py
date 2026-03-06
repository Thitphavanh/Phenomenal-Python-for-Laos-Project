from django.contrib import admin
from .models import (
    ChatConversation,
    ChatMessage,
    CourseAnalytics,
    PaymentSlipAnalysis,
    CourseRecommendation,
    VectorDocument,
)

@admin.register(ChatConversation)
class ChatConversationAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'user', 'started_at', 'last_message_at', 'is_active')
    list_filter = ('is_active', 'started_at', 'last_message_at')
    search_fields = ('session_id', 'user__username')
    readonly_fields = ('started_at', 'last_message_at')


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'role', 'content_snippet', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('content',)
    readonly_fields = ('created_at',)

    def content_snippet(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_snippet.short_description = 'Content'


@admin.register(CourseAnalytics)
class CourseAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('course', 'student_engagement_score', 'completion_rate_prediction', 'is_current', 'generated_at')
    list_filter = ('is_current', 'generated_at')
    search_fields = ('course__title',)
    readonly_fields = ('generated_at',)


@admin.register(PaymentSlipAnalysis)
class PaymentSlipAnalysisAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'transaction_id', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'processed_at')
    search_fields = ('transaction_id', 'sender_name', 'user__username')
    readonly_fields = ('created_at', 'processed_at')


@admin.register(CourseRecommendation)
class CourseRecommendationAdmin(admin.ModelAdmin):
    list_display = ('user', 'recommended_course', 'relevance_score', 'was_viewed', 'was_enrolled', 'is_active')
    list_filter = ('is_active', 'was_viewed', 'was_enrolled', 'generated_at')
    search_fields = ('user__username', 'recommended_course__title', 'reason')
    readonly_fields = ('generated_at', 'viewed_at')


@admin.register(VectorDocument)
class VectorDocumentAdmin(admin.ModelAdmin):
    list_display = ('document_type', 'document_id', 'vector_id', 'collection_name', 'updated_at')
    list_filter = ('document_type', 'collection_name')
    search_fields = ('vector_id', 'content')
    readonly_fields = ('created_at', 'updated_at')
