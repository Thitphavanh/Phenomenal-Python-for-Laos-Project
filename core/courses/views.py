from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.utils import timezone

from .models import (
    Course, Lesson, Enrollment, PricingPlan,
    CourseChapter, LessonProgress
)
from blog.models import Category, Tag


def course_list(request):
    """Display list of all published courses with filters"""
    courses = Course.objects.filter(status='published').select_related(
        'instructor', 'category'
    ).prefetch_related('tags')

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(short_description__icontains=search_query)
        )

    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        courses = courses.filter(category__slug=category_slug)

    # Filter by difficulty
    difficulty = request.GET.get('difficulty')
    if difficulty:
        courses = courses.filter(difficulty=difficulty)

    # Filter by price type
    price_filter = request.GET.get('price')
    if price_filter == 'free':
        courses = courses.filter(is_free=True)
    elif price_filter == 'paid':
        courses = courses.filter(is_free=False)

    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    allowed_sorts = ['-created_at', 'title', '-total_students', 'price']
    if sort_by in allowed_sorts:
        courses = courses.order_by(sort_by)

    # Get featured courses
    featured_courses = Course.objects.filter(
        status='published', is_featured=True
    )[:3]

    # Get categories for filter
    categories = Category.objects.all()

    # Pagination
    paginator = Paginator(courses, 12)  # Show 12 courses per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'featured_courses': featured_courses,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_slug,
        'selected_difficulty': difficulty,
        'selected_price': price_filter,
        'selected_sort': sort_by,
    }

    return render(request, 'courses/course_list.html', context)


def course_detail(request, slug):
    """Display detailed information about a course"""
    course = get_object_or_404(
        Course.objects.select_related('instructor', 'category')
        .prefetch_related('tags', 'chapters__lessons'),
        slug=slug,
        status='published'
    )

    # Get course chapters with lessons
    chapters = course.chapters.filter(is_published=True).prefetch_related('lessons')

    # Check if user is enrolled
    is_enrolled = False
    enrollment = None
    if request.user.is_authenticated:
        try:
            enrollment = Enrollment.objects.get(
                student=request.user,
                course=course
            )
            is_enrolled = True
        except Enrollment.DoesNotExist:
            pass

    # Get related courses
    related_courses = Course.objects.filter(
        status='published',
        category=course.category
    ).exclude(id=course.id)[:3]

    context = {
        'course': course,
        'chapters': chapters,
        'is_enrolled': is_enrolled,
        'enrollment': enrollment,
        'related_courses': related_courses,
        'objectives_list': course.get_objectives_list(),
        'prerequisites_list': course.get_prerequisites_list(),
    }

    return render(request, 'courses/course_detail.html', context)


@login_required
def lesson_detail(request, course_slug, lesson_slug):
    """Display lesson content (only for enrolled students)"""
    course = get_object_or_404(Course, slug=course_slug, status='published')
    lesson = get_object_or_404(
        Lesson,
        course=course,
        slug=lesson_slug,
        is_published=True
    )

    # Check enrollment or preview access
    is_enrolled = False
    enrollment = None

    try:
        enrollment = Enrollment.objects.get(
            student=request.user,
            course=course
        )
        is_enrolled = True
    except Enrollment.DoesNotExist:
        if not lesson.is_preview:
            messages.error(
                request,
                'ທ່ານຕ້ອງລົງທະບຽນຄອດສຶກສານີ້ກ່ອນຈຶ່ງຈະເບິ່ງບົດຮຽນໄດ້.'
            )
            return redirect('courses:course_detail', slug=course_slug)

    # Get or create lesson progress
    lesson_progress = None
    if is_enrolled:
        lesson_progress, created = LessonProgress.objects.get_or_create(
            enrollment=enrollment,
            lesson=lesson
        )

    # Get all lessons for navigation
    all_lessons = course.lessons.filter(is_published=True).order_by('chapter__order', 'order')
    lesson_list = list(all_lessons)

    # Find previous and next lessons
    current_index = lesson_list.index(lesson)
    previous_lesson = lesson_list[current_index - 1] if current_index > 0 else None
    next_lesson = lesson_list[current_index + 1] if current_index < len(lesson_list) - 1 else None

    # Get course chapters with lessons for sidebar
    chapters = course.chapters.filter(is_published=True).prefetch_related('lessons')

    context = {
        'course': course,
        'lesson': lesson,
        'enrollment': enrollment,
        'lesson_progress': lesson_progress,
        'previous_lesson': previous_lesson,
        'next_lesson': next_lesson,
        'all_lessons': all_lessons,
        'chapters': chapters,
    }

    return render(request, 'courses/lesson_detail.html', context)


@login_required
def mark_lesson_complete(request, course_slug, lesson_slug):
    """Mark a lesson as completed"""
    if request.method != 'POST':
        return redirect('courses:course_detail', slug=course_slug)

    course = get_object_or_404(Course, slug=course_slug)
    lesson = get_object_or_404(Lesson, course=course, slug=lesson_slug)

    try:
        enrollment = Enrollment.objects.get(
            student=request.user,
            course=course
        )
    except Enrollment.DoesNotExist:
        messages.error(request, 'ທ່ານຍັງບໍ່ໄດ້ລົງທະບຽນຄອດສຶກສານີ້.')
        return redirect('courses:course_detail', slug=course_slug)

    # Get or create lesson progress and mark as complete
    lesson_progress, created = LessonProgress.objects.get_or_create(
        enrollment=enrollment,
        lesson=lesson
    )

    lesson_progress.mark_completed()

    messages.success(request, f'ບົດຮຽນ "{lesson.title}" ຖືກໝາຍວ່າສຳເລັດແລ້ວ!')

    # Redirect to next lesson or course detail
    all_lessons = list(course.lessons.filter(is_published=True).order_by('chapter__order', 'order'))
    current_index = all_lessons.index(lesson)

    if current_index < len(all_lessons) - 1:
        next_lesson = all_lessons[current_index + 1]
        return redirect('courses:lesson_detail', course_slug=course_slug, lesson_slug=next_lesson.slug)
    else:
        messages.success(request, 'ຂໍສະແດງຄວາມຍິນດີ! ທ່ານໄດ້ຮຽນຈົບຄອດສຶກສານີ້ແລ້ວ!')
        return redirect('courses:course_detail', slug=course_slug)


@login_required
def enroll_course(request, slug):
    """Enroll user in a course or show enrollment page"""
    course = get_object_or_404(Course, slug=slug, status='published')

    # Check if already enrolled
    try:
        enrollment = Enrollment.objects.get(
            student=request.user,
            course=course
        )
        # Already enrolled - go to first lesson
        first_lesson = course.lessons.filter(is_published=True).order_by('chapter__order', 'order').first()
        if first_lesson:
            return redirect('courses:lesson_detail', course_slug=slug, lesson_slug=first_lesson.slug)
        else:
            return redirect('courses:course_detail', slug=slug)
    except Enrollment.DoesNotExist:
        # Not enrolled - show enrollment/registration page
        pass

    # If POST request, create enrollment
    if request.method == 'POST':
        enrollment = Enrollment.objects.create(
            student=request.user,
            course=course,
            payment_amount=course.price if not course.is_free else 0,
            payment_date=timezone.now() if course.is_free else None,
        )

        # Update course student count
        course.total_students += 1
        course.save()

        messages.success(
            request,
            f'ລົງທະບຽນສຳເລັດ! ຍິນດີຕ້ອນຮັບສູ່ຄອດສຶກສາ "{course.title}"'
        )

        # Redirect to first lesson
        first_lesson = course.lessons.filter(is_published=True).order_by('chapter__order', 'order').first()
        if first_lesson:
            return redirect('courses:lesson_detail', course_slug=slug, lesson_slug=first_lesson.slug)
        else:
            return redirect('courses:course_detail', slug=slug)

    # GET request - show enrollment page
    context = {
        'course': course,
        'objectives_list': course.get_objectives_list(),
        'prerequisites_list': course.get_prerequisites_list(),
    }

    return render(request, 'courses/enroll_course.html', context)


@login_required
def my_courses(request):
    """Display user's enrolled courses"""
    enrollments = Enrollment.objects.filter(
        student=request.user
    ).select_related('course').order_by('-enrolled_at')

    context = {
        'enrollments': enrollments,
    }

    return render(request, 'courses/my_courses.html', context)


def pricing(request):
    """Display pricing plans"""
    pricing_plans = PricingPlan.objects.filter(is_active=True).order_by('price')

    # Get some featured courses
    featured_courses = Course.objects.filter(
        status='published',
        is_featured=True
    )[:6]

    context = {
        'pricing_plans': pricing_plans,
        'featured_courses': featured_courses,
    }

    return render(request, 'courses/pricing.html', context)


def instructor_profile(request, username):
    """Display instructor profile with their courses"""
    from django.contrib.auth.models import User

    instructor = get_object_or_404(User, username=username)

    # Get instructor's published courses
    courses = Course.objects.filter(
        instructor=instructor,
        status='published'
    ).order_by('-created_at')

    # Get stats
    total_students = sum(course.total_students for course in courses)
    total_courses = courses.count()

    context = {
        'instructor': instructor,
        'courses': courses,
        'total_students': total_students,
        'total_courses': total_courses,
    }

    return render(request, 'courses/instructor_profile.html', context)
