from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class DocCategory(models.Model):
    """Category model specifically for Documentation"""
    name = models.CharField(max_length=100, unique=True)
    name_lao = models.CharField(max_length=100, blank=True, null=True, help_text="Lao language name")
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, help_text="Category description")
    icon = models.CharField(max_length=50, blank=True, help_text="Icon class or emoji")
    order = models.IntegerField(default=0, help_text="Display order")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Documentation Category"
        verbose_name_plural = "Documentation Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("docs:category_docs", args=[self.slug])


class Documentation(models.Model):
    """Model for Python/Django documentation and tutorials"""
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="documentations",
        null=True, blank=True
    )
    description = models.TextField(
        max_length=300,
        help_text="Brief description/excerpt of the documentation"
    )
    content = models.TextField(help_text="Main content (supports markdown)")

    # Organization
    category = models.ForeignKey(
        DocCategory, on_delete=models.SET_NULL, null=True, blank=True,
        help_text="Documentation category (e.g., Python Basics, Django Advanced)",
        related_name='documentations'
    )
    chapter_number = models.IntegerField(default=0, help_text="Chapter ordering")
    section_number = models.IntegerField(default=0, help_text="Section within chapter")

    # Difficulty and metadata
    difficulty_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        ],
        default='beginner'
    )

    # Media
    featured_image = models.ImageField(
        upload_to="docs/images/", blank=True, null=True
    )
    diagram_image = models.ImageField(
        upload_to="docs/diagrams/", blank=True, null=True
    )

    # Status and timestamps
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="published")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['chapter_number', 'section_number']
        verbose_name_plural = "Documentation"
        db_table = 'blog_documentation'  # Keep existing table

    def __str__(self):
        if self.chapter_number or self.section_number:
            return f"{self.chapter_number}.{self.section_number} - {self.title}"
        return self.title

    def get_absolute_url(self):
        return reverse("docs:doc_detail", args=[self.slug])

    def save(self, *args, **kwargs):
        if self.status == "published" and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
