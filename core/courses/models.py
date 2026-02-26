import re
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


def get_video_embed_data(url):
    """Parse video URL and return embed data (type and url)"""
    if not url:
        return None
    
    # YouTube
    youtube_regex = (
        r'(https?://)?(www\.)?'
        r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    youtube_match = re.match(youtube_regex, url)
    if youtube_match:
        return {
            'type': 'youtube',
            'url': f"https://www.youtube.com/embed/{youtube_match.group(6)}"
        }

    # Vimeo
    vimeo_regex = r'https?://(www\.)?vimeo.com/(\d+)(?:.*/)?$'
    vimeo_match = re.match(vimeo_regex, url)
    if vimeo_match:
        return {
            'type': 'vimeo',
            'url': f"https://player.vimeo.com/video/{vimeo_match.group(2)}"
        }

    # Native/Other
    return {
        'type': 'native',
        'url': url
    }


class PricingPlan(models.Model):
    """Pricing plans for courses (Free, Single Course, VIP)"""
    PLAN_TYPE_CHOICES = [
        ('free', 'Free'),
        ('single', 'Single Course'),
        ('vip', 'VIP Membership'),
    ]

    name = models.CharField(max_length=100)
    plan_type = models.CharField(max_length=10, choices=PLAN_TYPE_CHOICES, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    duration_days = models.IntegerField(
        default=0,
        help_text="0 = lifetime, 365 = 1 year, etc."
    )
    description = models.TextField()
    features = models.TextField(help_text="One feature per line")
    is_popular = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['price']
        db_table = 'blog_pricingplan'  # Keep existing table

    def __str__(self):
        return f"{self.name} - ${self.price}"

    def get_features_list(self):
        """Return features as a list"""
        return [f.strip() for f in self.features.split('\n') if f.strip()]

class Tag(models.Model):
    """Tag model for Courses"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        db_table = 'courses_tag'
        verbose_name = 'Course Tag'
        verbose_name_plural = 'Course Tags'

    def __str__(self):
        return self.name


class Category(models.Model):
    """Category model for Courses"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()

    class Meta:
        ordering = ['name']
        db_table = 'courses_category'
        verbose_name = 'Course Category'
        verbose_name_plural = 'Course Categories'

    def __str__(self):
        return self.name

class Course(models.Model):
    """Course model for online learning"""
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    # Basic Info
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    instructor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="courses"
    )
    short_description = models.TextField(max_length=300)
    description = models.TextField()

    # Media
    cover_image = models.ImageField(upload_to="courses/covers/", blank=True, null=True)

    # Preview Videos - Multiple Types Support
    preview_video_url_youtube = models.URLField(
        blank=True, null=True,
        help_text="YouTube video URL (e.g., https://www.youtube.com/watch?v=xxxxx)"
    )
    preview_video_url_vimeo = models.URLField(
        blank=True, null=True,
        help_text="Vimeo video URL (e.g., https://vimeo.com/xxxxx)"
    )
    preview_video_url_native = models.URLField(
        blank=True, null=True,
        help_text="Direct video URL (.mp4, .webm, etc.) or other video platform"
    )
    preview_video_file = models.FileField(
        upload_to="courses/previews/", blank=True, null=True,
        help_text="Upload a video file directly (mp4, webm, etc.)"
    )

    # Legacy field - kept for backward compatibility
    preview_video_url = models.URLField(blank=True, null=True)

    # Classification
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    tags = models.ManyToManyField(Tag, blank=True)
    difficulty = models.CharField(
        max_length=20, choices=DIFFICULTY_CHOICES, default='beginner'
    )

    # Pricing
    is_free = models.BooleanField(default=False)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        help_text="Price in USD (0 for free courses)"
    )

    # Metadata
    duration_hours = models.DecimalField(
        max_digits=5, decimal_places=2, default=0,
        help_text="Total course duration in hours"
    )
    total_lessons = models.IntegerField(default=0)
    total_students = models.IntegerField(default=0)

    # Learning Objectives
    learning_objectives = models.TextField(
        blank=True,
        help_text="One objective per line"
    )
    prerequisites = models.TextField(
        blank=True,
        help_text="One prerequisite per line"
    )

    # Status
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        db_table = 'blog_course'  # Keep existing table

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("courses:course_detail", args=[self.slug])

    def save(self, *args, **kwargs):
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def get_objectives_list(self):
        """Return learning objectives as a list"""
        return [obj.strip() for obj in self.learning_objectives.split('\n') if obj.strip()]

    def get_prerequisites_list(self):
        """Return prerequisites as a list"""
        return [pre.strip() for pre in self.prerequisites.split('\n') if pre.strip()]

    def update_total_lessons(self):
        """Update total lessons count"""
        self.total_lessons = self.lessons.filter(is_published=True).count()
        self.save()

    def update_duration(self):
        """Update total duration from lessons"""
        from django.db.models import Sum
        total_minutes = self.lessons.filter(is_published=True).aggregate(
            total=Sum('duration_minutes')
        )['total'] or 0
        self.duration_hours = total_minutes / 60
        self.save()

    def get_video_context(self):
        """Get preview video embed context - supports multiple video types"""
        # Priority order: File upload > YouTube > Vimeo > Native URL > Legacy URL
        if self.preview_video_file:
            return {'type': 'native', 'url': self.preview_video_file.url}

        if self.preview_video_url_youtube:
            return get_video_embed_data(self.preview_video_url_youtube)

        if self.preview_video_url_vimeo:
            return get_video_embed_data(self.preview_video_url_vimeo)

        if self.preview_video_url_native:
            return {'type': 'native', 'url': self.preview_video_url_native}

        # Fallback to legacy field
        return get_video_embed_data(self.preview_video_url)


class CourseChapter(models.Model):
    """Course chapters/sections"""
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="chapters"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['course', 'order']
        unique_together = ['course', 'order']
        db_table = 'blog_coursechapter'  # Keep existing table

    def __str__(self):
        return f"{self.course.title} - Chapter {self.order}: {self.title}"


class Lesson(models.Model):
    """Individual lessons within a course"""
    CONTENT_TYPE_CHOICES = [
        ('video', 'Video'),
        ('text', 'Text/Article'),
        ('quiz', 'Quiz'),
        ('file', 'Downloadable File'),
    ]

    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="lessons"
    )
    chapter = models.ForeignKey(
        CourseChapter, on_delete=models.CASCADE, related_name="lessons",
        null=True, blank=True
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField(blank=True)

    # Content
    content_type = models.CharField(
        max_length=10, choices=CONTENT_TYPE_CHOICES, default='video'
    )

    # Lesson Videos - Multiple Types Support
    video_url_youtube = models.URLField(
        blank=True, null=True,
        help_text="YouTube video URL (e.g., https://www.youtube.com/watch?v=xxxxx)"
    )
    video_url_vimeo = models.URLField(
        blank=True, null=True,
        help_text="Vimeo video URL (e.g., https://vimeo.com/xxxxx)"
    )
    video_url_native = models.URLField(
        blank=True, null=True,
        help_text="Direct video URL (.mp4, .webm, etc.) or other video platform"
    )
    video_file = models.FileField(
        upload_to="courses/lessons/", blank=True, null=True,
        help_text="Upload a video file directly (mp4, webm, etc.)"
    )

    # Legacy field - kept for backward compatibility
    video_url = models.URLField(blank=True, null=True)

    content = models.TextField(blank=True)
    attachments = models.FileField(
        upload_to="courses/attachments/", blank=True, null=True
    )

    # Metadata
    duration_minutes = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    is_preview = models.BooleanField(
        default=False,
        help_text="Can be viewed without enrollment"
    )
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['course', 'chapter', 'order']
        unique_together = ['course', 'slug']
        db_table = 'blog_lesson'  # Keep existing table

    def __str__(self):
        if self.chapter:
            return f"{self.chapter.title} - {self.order}. {self.title}"
        return f"{self.course.title} - {self.title}"

    def get_absolute_url(self):
        return reverse("courses:lesson_detail", args=[self.course.slug, self.slug])

    def get_video_context(self):
        """Get lesson video embed context - supports multiple video types"""
        # Priority order: File upload > YouTube > Vimeo > Native URL > Legacy URL
        if self.video_file:
            return {'type': 'native', 'url': self.video_file.url}

        if self.video_url_youtube:
            return get_video_embed_data(self.video_url_youtube)

        if self.video_url_vimeo:
            return get_video_embed_data(self.video_url_vimeo)

        if self.video_url_native:
            return {'type': 'native', 'url': self.video_url_native}

        # Fallback to legacy field
        return get_video_embed_data(self.video_url)


class Enrollment(models.Model):
    """Student enrollments in courses"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="enrollments"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="enrollments"
    )
    pricing_plan = models.ForeignKey(
        PricingPlan, on_delete=models.SET_NULL, null=True, blank=True
    )

    # Progress
    progress_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, default=0
    )
    completed_lessons = models.ManyToManyField(
        Lesson, blank=True, related_name="completed_by"
    )

    # Status
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    # Payment
    payment_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    payment_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['student', 'course']
        ordering = ['-enrolled_at']
        db_table = 'blog_enrollment'  # Keep existing table

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"

    def update_progress(self):
        """Calculate and update progress percentage"""
        total_lessons = self.course.lessons.filter(is_published=True).count()
        if total_lessons > 0:
            completed = self.completed_lessons.count()
            self.progress_percentage = (completed / total_lessons) * 100
            if self.progress_percentage >= 100 and not self.completed_at:
                self.completed_at = timezone.now()
                self.status = 'completed'
            self.save()


class LessonProgress(models.Model):
    """Track individual lesson progress"""
    enrollment = models.ForeignKey(
        Enrollment, on_delete=models.CASCADE, related_name="lesson_progress"
    )
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    watch_duration = models.IntegerField(default=0, help_text="Seconds watched")
    completed_at = models.DateTimeField(null=True, blank=True)
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['enrollment', 'lesson']
        ordering = ['lesson__order']
        db_table = 'blog_lessonprogress'  # Keep existing table

    def __str__(self):
        return f"{self.enrollment.student.username} - {self.lesson.title}"

    def mark_completed(self):
        """Mark lesson as completed"""
        if not self.is_completed:
            self.is_completed = True
            self.completed_at = timezone.now()
            self.save()
            # Add to enrollment's completed lessons
            self.enrollment.completed_lessons.add(self.lesson)
            self.enrollment.update_progress()
