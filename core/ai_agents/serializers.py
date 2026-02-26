"""
Django REST Framework Serializers for AI Agents
Serializers ສຳລັບ API endpoints
"""

from rest_framework import serializers
from .models import (
    ChatConversation,
    ChatMessage,
    CourseAnalytics,
    PaymentSlipAnalysis,
    CourseRecommendation,
    VectorDocument
)
from django.contrib.auth.models import User
from courses.models import Course


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class ChatMessageSerializer(serializers.ModelSerializer):
    """Serializer for chat messages"""
    class Meta:
        model = ChatMessage
        fields = ['id', 'role', 'content', 'metadata', 'created_at']
        read_only_fields = ['id', 'created_at']


class ChatConversationSerializer(serializers.ModelSerializer):
    """Serializer for chat conversations"""
    messages = ChatMessageSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ChatConversation
        fields = [
            'id', 'user', 'session_id', 'started_at',
            'last_message_at', 'is_active', 'messages'
        ]
        read_only_fields = ['id', 'session_id', 'started_at', 'last_message_at']


class ChatRequestSerializer(serializers.Serializer):
    """Serializer for chat requests"""
    message = serializers.CharField(required=True, max_length=2000)
    session_id = serializers.CharField(required=False, max_length=100)
    use_rag = serializers.BooleanField(default=True)
    provider = serializers.ChoiceField(
        choices=['openai', 'anthropic'],
        default='openai',
        required=False
    )


class ChatResponseSerializer(serializers.Serializer):
    """Serializer for chat responses"""
    response = serializers.CharField()
    session_id = serializers.CharField()
    sources = serializers.ListField(child=serializers.DictField(), required=False)
    tokens_used = serializers.IntegerField(required=False)
    model = serializers.CharField(required=False)
    provider = serializers.CharField(required=False)


class CourseSerializer(serializers.ModelSerializer):
    """Simple course serializer"""
    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 'short_description', 'difficulty', 'is_free', 'price']


class CourseAnalyticsSerializer(serializers.ModelSerializer):
    """Serializer for course analytics"""
    course = CourseSerializer(read_only=True)
    
    class Meta:
        model = CourseAnalytics
        fields = [
            'id', 'course', 'enrollment_prediction', 'performance_insights',
            'student_engagement_score', 'completion_rate_prediction',
            'recommendations', 'suggested_improvements',
            'generated_at', 'is_current'
        ]
        read_only_fields = ['id', 'generated_at']


class PaymentSlipAnalysisSerializer(serializers.ModelSerializer):
    """Serializer for payment slip analysis"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = PaymentSlipAnalysis
        fields = [
            'id', 'image', 'extracted_data', 'amount', 'transaction_id',
            'payment_date', 'sender_name', 'confidence_score', 'status',
            'notes', 'user', 'event_registration', 'created_at', 'processed_at'
        ]
        read_only_fields = [
            'id', 'extracted_data', 'amount', 'transaction_id',
            'payment_date', 'sender_name', 'confidence_score',
            'created_at', 'processed_at'
        ]


class PaymentSlipUploadSerializer(serializers.Serializer):
    """Serializer for payment slip upload"""
    image = serializers.ImageField(required=True)
    event_registration_id = serializers.IntegerField(required=False)


class CourseRecommendationSerializer(serializers.ModelSerializer):
    """Serializer for course recommendations"""
    user = UserSerializer(read_only=True)
    recommended_course = CourseSerializer(read_only=True)
    
    class Meta:
        model = CourseRecommendation
        fields = [
            'id', 'user', 'recommended_course', 'relevance_score',
            'reason', 'based_on', 'was_viewed', 'was_enrolled',
            'viewed_at', 'generated_at', 'is_active'
        ]
        read_only_fields = ['id', 'generated_at']


class RecommendationRequestSerializer(serializers.Serializer):
    """Serializer for recommendation requests"""
    limit = serializers.IntegerField(default=5, min_value=1, max_value=20)


class VectorDocumentSerializer(serializers.ModelSerializer):
    """Serializer for vector documents"""
    class Meta:
        model = VectorDocument
        fields = [
            'id', 'document_type', 'document_id', 'content',
            'vector_id', 'collection_name', 'metadata',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'vector_id', 'created_at', 'updated_at']


class AnalyticsRequestSerializer(serializers.Serializer):
    """Serializer for analytics requests"""
    course_id = serializers.IntegerField(required=True)
    generate_report = serializers.BooleanField(default=True)


class AnalyticsResponseSerializer(serializers.Serializer):
    """Serializer for analytics responses"""
    basic_stats = serializers.DictField()
    enrollment_trends = serializers.DictField()
    completion_analysis = serializers.DictField()
    engagement_score = serializers.FloatField()
    predictions = serializers.DictField()
    recommendations = serializers.ListField(child=serializers.CharField())
