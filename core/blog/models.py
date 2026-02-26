from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from ckeditor.fields import RichTextField


class Category(models.Model):
    """Shared category model for Blog, Docs, and Courses"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("blog:category_posts", args=[self.slug])


class Tag(models.Model):
    """Shared tag model for Blog, Docs, and Courses"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    """Model for blog posts and community posts (Reddit-style)"""
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]

    TYPE_CHOICES = [
        ("post", "Community Post"),
        ("blog", "Blog Article"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    post_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default="post")
    content = RichTextField(help_text="Rich text content for posts and blogs")
    excerpt = models.TextField(
        max_length=300, help_text="Brief description of the post"
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    tags = models.ManyToManyField(Tag, blank=True)
    featured_image = models.ImageField(upload_to="blog/images/", blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.slug])

    def save(self, *args, **kwargs):
        if self.status == "published" and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def get_vote_score(self):
        """Calculate total vote score (upvotes - downvotes)"""
        from django.db.models import Sum
        score = self.votes.aggregate(
            total=Sum('vote_type')
        )['total']
        return score if score is not None else 0

    def get_upvotes(self):
        """Get count of upvotes"""
        return self.votes.filter(vote_type=1).count()

    def get_downvotes(self):
        """Get count of downvotes"""
        return self.votes.filter(vote_type=-1).count()


class Comment(models.Model):
    """Comments on blog posts"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"


class PostVote(models.Model):
    """Reddit-style voting system for posts"""
    VOTE_CHOICES = [
        (1, 'Upvote'),
        (-1, 'Downvote'),
    ]

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    vote_type = models.IntegerField(choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['post', 'user'], ['post', 'session_key']]
        indexes = [
            models.Index(fields=['post', 'vote_type']),
        ]

    def __str__(self):
        return f"{self.get_vote_type_display()} on {self.post.title}"
