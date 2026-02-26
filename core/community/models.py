from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
import uuid

class Topic(models.Model):
    """A discussion thread/topic in the community"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topics')
    
    # Status
    is_pinned = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    is_solved = models.BooleanField(default=False)
    
    # Metadata
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Relations
    # We can reuse the Category model from blog or create a new one. 
    # For simplicity and separation, let's reuse 'blog.Category' or just use a simple CharField for tags/category if needed.
    # But clean design suggests referencing a category. Let's import from blog for now to keep it unified across site?
    # Or create a simple Category model here? Let's use blog.Category to keep "Python", "Django" tags consistent.
    category = models.ForeignKey('blog.Category', on_delete=models.SET_NULL, null=True, blank=True, related_name='community_topics')

    class Meta:
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) + "-" + str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('community:topic_detail', args=[self.slug])

class Reply(models.Model):
    """A reply to a topic"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies')
    
    is_accepted_answer = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Reply by {self.author} on {self.topic}"
