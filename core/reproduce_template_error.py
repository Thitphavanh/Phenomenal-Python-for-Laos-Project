import os
import django
from django.conf import settings
from django.template.loader import render_to_string
from django.test import RequestFactory

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.dev')
django.setup()

import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from courses.models import Course, Lesson
from django.contrib.auth.models import User

def reproduce_error():
    print("Attempting to reproduce template rendering error...")
    
    # Mock context data
    # We'll try to get actual objects if they exist, otherwise we'll mock them
    try:
        # Try to get the first course and lesson, or create dummy ones in memory if possible
        # For reproduction, it's safer to use existing data if available, but we want to avoid DB writes
        # so we will just fetch.
        
        course = Course.objects.first()
        if not course:
            print("No courses found in DB. Creating a dummy course instance (not saved).")
            course = Course(title="Dummy Course", slug="dummy-course")
            
        lesson = Lesson.objects.filter(course=course).first()
        if not lesson:
             print("No lessons found for course. Creating a dummy lesson instance (not saved).")
             lesson = Lesson(title="Dummy Lesson", slug="dummy-lesson", course=course, content="<p>Test content</p>")

        # Create a mock request
        factory = RequestFactory()
        request = factory.get(f'/courses/{course.slug}/lesson/{lesson.slug}/')
        request.user = User.objects.first() or User(username='testuser')
        request.resolver_match = type('obj', (object,), {'app_name': 'courses', 'url_name': 'lesson_detail'})
        
        context = {
            'course': course,
            'lesson': lesson,
            'enrollment': None,
            'lesson_progress': None,
            'previous_lesson': None,
            'next_lesson': None,
            'all_lessons': [],
            'request': request, # Template rendering needs request context usually
        }

        print(f"Rendering template 'courses/lesson_detail.html' with context...")
        rendered = render_to_string('courses/lesson_detail.html', context, request=request)
        print("Template rendered successfully!")
        print("Output length:", len(rendered))
        
    except Exception as e:
        print("\n!!! ERROR CAUGHT !!!")
        print("Type:", type(e).__name__)
        print("Message:", str(e))
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    reproduce_error()
