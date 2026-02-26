from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ChatConversation(models.Model):
    """Track chat conversations with AI"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_conversations', null=True, blank=True)
    session_id = models.CharField(max_length=100, unique=True)
    started_at = models.DateTimeField(auto_now_add=True)
    last_message_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-last_message_at']

    def __str__(self):
        user_name = self.user.username if self.user else f"Guest-{self.session_id[:8]}"
        return f"Chat {self.id} - {user_name}"


class ChatMessage(models.Model):
    """Individual messages in a conversation"""
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
        ('system', 'System'),
    ]

    conversation = models.ForeignKey(ChatConversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    metadata = models.JSONField(null=True, blank=True, help_text="Additional context like sources, tokens used, etc.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."


class CourseAnalytics(models.Model):
    """Store AI-generated analytics for courses"""
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='ai_analytics')

    # Analytics Data
    enrollment_prediction = models.JSONField(null=True, blank=True)
    performance_insights = models.JSONField(null=True, blank=True)
    student_engagement_score = models.FloatField(default=0)
    completion_rate_prediction = models.FloatField(default=0)

    # AI Recommendations
    recommendations = models.TextField(blank=True)
    suggested_improvements = models.JSONField(null=True, blank=True)

    # Metadata
    generated_at = models.DateTimeField(auto_now=True)
    is_current = models.BooleanField(default=True)

    class Meta:
        ordering = ['-generated_at']
        verbose_name_plural = "Course Analytics"

    def __str__(self):
        return f"Analytics for {self.course.title}"


class PaymentSlipAnalysis(models.Model):
    """AI analysis of payment slips"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    # Payment slip image
    image = models.ImageField(upload_to='payment_slips/')

    # Extracted Information
    extracted_data = models.JSONField(null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True)
    payment_date = models.DateField(null=True, blank=True)
    sender_name = models.CharField(max_length=200, blank=True)

    # AI Analysis
    confidence_score = models.FloatField(default=0, help_text="AI confidence in extraction (0-1)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)

    # Relations
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_analyses', null=True, blank=True)
    event_registration = models.ForeignKey('events.EventRegistration', on_delete=models.SET_NULL, null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Payment Slip Analyses"

    def __str__(self):
        return f"Payment Slip Analysis #{self.id}"


class CourseRecommendation(models.Model):
    """AI-generated course recommendations for users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_recommendations')
    recommended_course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)

    # Recommendation Details
    relevance_score = models.FloatField(default=0, help_text="How relevant is this course (0-1)")
    reason = models.TextField(help_text="Why this course is recommended")
    based_on = models.JSONField(null=True, blank=True, help_text="What factors influenced this recommendation")

    # User Interaction
    was_viewed = models.BooleanField(default=False)
    was_enrolled = models.BooleanField(default=False)
    viewed_at = models.DateTimeField(null=True, blank=True)

    # Metadata
    generated_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-relevance_score', '-generated_at']
        unique_together = ['user', 'recommended_course']

    def __str__(self):
        return f"{self.user.username} -> {self.recommended_course.title} ({self.relevance_score:.2f})"


class VectorDocument(models.Model):
    """Track documents stored in vector database"""
    DOCUMENT_TYPE_CHOICES = [
        ('course', 'Course'),
        ('blog', 'Blog Post'),
        ('doc', 'Documentation'),
        ('event', 'Event'),
    ]

    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES)
    document_id = models.IntegerField(help_text="ID of the source document")
    content = models.TextField(help_text="Original content")

    # Vector DB Information
    vector_id = models.CharField(max_length=200, unique=True)
    collection_name = models.CharField(max_length=100)

    # Metadata
    metadata = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['document_type', 'document_id']),
        ]

    def __str__(self):
        return f"{self.document_type} - {self.document_id}"
