from django.contrib import admin
from .models import (
    Tag, Category, PricingPlan, Course, CourseChapter, Lesson,
    Enrollment, LessonProgress
)


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ('title', 'slug', 'content_type', 'duration_minutes', 'order', 'is_preview', 'is_published')
    prepopulated_fields = {"slug": ("title",)}


class CourseChapterInline(admin.TabularInline):
    model = CourseChapter
    extra = 1
    fields = ('title', 'order', 'is_published')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name', 'slug']
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name', 'description']
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description')
        }),
    )


@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'plan_type', 'price', 'duration_days', 'is_popular', 'is_active']
    list_filter = ['plan_type', 'is_popular', 'is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_popular', 'is_active']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'instructor', 'category', 'difficulty', 'is_free',
        'price', 'total_students', 'status', 'is_featured', 'created_at'
    ]
    list_filter = ['status', 'difficulty', 'is_free', 'is_featured', 'category', 'created_at']
    search_fields = ['title', 'description', 'short_description']
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ('tags',)
    date_hierarchy = 'created_at'
    list_editable = ['status', 'is_featured']
    inlines = [CourseChapterInline, LessonInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'instructor', 'short_description', 'description')
        }),
        ('Media', {
            'fields': (
                'cover_image',
                'preview_video_url_youtube',
                'preview_video_url_vimeo',
                'preview_video_url_native',
                'preview_video_file',
                'preview_video_url',  # Legacy field
            ),
            'description': 'ເລືອກວິທີການເພີ່ມວິດີໂອ: YouTube URL, Vimeo URL, Native URL, ຫຼື Upload ໄຟລ໌ວິດີໂອ'
        }),
        ('Classification', {
            'fields': ('category', 'tags', 'difficulty')
        }),
        ('Pricing', {
            'fields': ('is_free', 'price')
        }),
        ('Metadata', {
            'fields': ('duration_hours', 'total_lessons', 'total_students')
        }),
        ('Learning Details', {
            'fields': ('learning_objectives', 'prerequisites'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('status', 'is_featured', 'published_at')
        }),
    )


@admin.register(CourseChapter)
class CourseChapterAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'is_published', 'created_at']
    list_filter = ['course', 'is_published', 'created_at']
    search_fields = ['title', 'description', 'course__title']
    list_editable = ['order', 'is_published']
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'course', 'chapter', 'content_type', 'duration_minutes',
        'order', 'is_preview', 'is_published', 'created_at'
    ]
    list_filter = ['course', 'chapter', 'content_type', 'is_preview', 'is_published', 'created_at']
    search_fields = ['title', 'description', 'course__title']
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ['order', 'is_preview', 'is_published']

    fieldsets = (
        ('Basic Information', {
            'fields': ('course', 'chapter', 'title', 'slug', 'description')
        }),
        ('Content', {
            'fields': (
                'content_type',
                'video_url_youtube',
                'video_url_vimeo',
                'video_url_native',
                'video_file',
                'video_url',  # Legacy field
                'content',
                'attachments'
            ),
            'description': 'ເລືອກວິທີການເພີ່ມວິດີໂອ: YouTube URL, Vimeo URL, Native URL, ຫຼື Upload ໄຟລ໌ວິດີໂອ'
        }),
        ('Metadata', {
            'fields': ('duration_minutes', 'order', 'is_preview', 'is_published')
        }),
    )


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = [
        'student', 'course', 'pricing_plan', 'progress_percentage',
        'status', 'enrolled_at', 'payment_amount'
    ]
    list_filter = ['status', 'pricing_plan', 'enrolled_at']
    search_fields = ['student__username', 'course__title']
    filter_horizontal = ('completed_lessons',)
    readonly_fields = ('enrolled_at', 'completed_at')

    fieldsets = (
        ('Enrollment Info', {
            'fields': ('student', 'course', 'pricing_plan')
        }),
        ('Progress', {
            'fields': ('progress_percentage', 'completed_lessons')
        }),
        ('Status', {
            'fields': ('status', 'enrolled_at', 'completed_at', 'expires_at')
        }),
        ('Payment', {
            'fields': ('payment_amount', 'payment_date')
        }),
    )


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = [
        'enrollment', 'lesson', 'is_completed', 'watch_duration',
        'completed_at', 'last_accessed'
    ]
    list_filter = ['is_completed', 'completed_at', 'last_accessed']
    search_fields = [
        'enrollment__student__username',
        'lesson__title',
        'enrollment__course__title'
    ]
    readonly_fields = ('completed_at', 'last_accessed')
