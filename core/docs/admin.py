from django.contrib import admin
from django import forms
from .models import Documentation, DocCategory


@admin.register(DocCategory)
class DocCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "name_lao", "slug", "order", "is_active", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["name", "name_lao", "slug", "description"]
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ["order", "is_active"]
    ordering = ["order", "name"]

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'name_lao', 'slug', 'description')
        }),
        ('Display Settings', {
            'fields': ('icon', 'order', 'is_active')
        }),
    )


class DocumentationAdminForm(forms.ModelForm):
    """Custom form for Documentation admin to handle markdown content"""

    class Meta:
        model = Documentation
        fields = '__all__'
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 30,
                'cols': 100,
                'style': 'font-family: monospace; font-size: 13px;',
                'placeholder': 'Enter markdown content here...\n\n## Example Heading\n\nYour content...\n\n```python\nprint("Hello")\n```'
            }),
            'description': forms.Textarea(attrs={'rows': 3}),
        }


@admin.register(Documentation)
class DocumentationAdmin(admin.ModelAdmin):
    form = DocumentationAdminForm
    list_display = [
        "title", "category", "difficulty_level", "chapter_number",
        "section_number", "status", "is_published", "created_at"
    ]
    list_filter = ["category", "difficulty_level", "status", "is_published", "created_at"]
    search_fields = ["title", "content", "description"]
    prepopulated_fields = {"slug": ("title",)}
    ordering = ["chapter_number", "section_number"]
    list_editable = ["is_published", "status"]
    date_hierarchy = "published_at"

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'status')
        }),
        ('Content', {
            'fields': ('description', 'content'),
            'description': 'Use Markdown syntax for content. Will be rendered with syntax highlighting.'
        }),
        ('Organization', {
            'fields': ('category', 'chapter_number', 'section_number', 'difficulty_level')
        }),
        ('Media', {
            'fields': ('featured_image', 'diagram_image'),
            'classes': ('collapse',)
        }),
        ('Publishing', {
            'fields': ('is_published', 'published_at'),
            'classes': ('collapse',)
        }),
    )
