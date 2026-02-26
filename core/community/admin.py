from django.contrib import admin
from .models import Topic, Reply

class ReplyInline(admin.TabularInline):
    model = Reply
    extra = 1

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_solved', 'is_closed', 'created_at', 'views_count')
    list_filter = ('is_solved', 'is_closed', 'is_pinned', 'category', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    prepopulated_fields = {} # Slug is auto-generated in save
    inlines = [ReplyInline]

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('author', 'topic', 'is_accepted_answer', 'created_at')
    list_filter = ('is_accepted_answer', 'created_at')
    search_fields = ('content', 'author__username', 'topic__title')
