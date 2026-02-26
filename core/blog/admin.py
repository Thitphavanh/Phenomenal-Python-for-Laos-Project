from django.contrib import admin
from django import forms
from django.db import models
from .models import Post, Category, Tag, Comment, PostVote


@admin.register(PostVote)
class PostVoteAdmin(admin.ModelAdmin):
    list_display = ["post", "user", "vote_type", "created_at"]
    list_filter = ["vote_type", "created_at"]
    search_fields = ["post__title", "user__username"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "post_type", "author", "status", "created_at", "published_at"]
    list_filter = ["post_type", "status", "created_at", "category", "tags"]
    search_fields = ["title", "content", "excerpt"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    ordering = ["-created_at"]
    filter_horizontal = ("tags",)

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'post_type', 'status')
        }),
        ('Content', {
            'fields': ('content', 'excerpt'),
            'description': 'Rich text editor for posts and blog articles.'
        }),
        ('Categorization', {
            'fields': ('category', 'tags')
        }),
        ('Media', {
            'fields': ('featured_image',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('published_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["name", "post", "created_at", "active"]
    list_filter = ["active", "created_at"]
    search_fields = ["name", "email", "content"]
    actions = ["approve_comments"]

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
