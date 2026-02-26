import os
import django
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from events.models import EventCategory, Event

def populate():
    # Get organizer
    admin_user = User.objects.first()
    if not admin_user:
        print("Error: No users found. Please create a superuser first.")
        return

    # Create Categories
    categories = [
        {'name': 'Workshop', 'slug': 'workshop', 'color': 'blue', 'icon': 'academic-cap'},
        {'name': 'Meetup', 'slug': 'meetup', 'color': 'green', 'icon': 'users'},
        {'name': 'Conference', 'slug': 'conference', 'color': 'purple', 'icon': 'microphone'},
        {'name': 'Hackathon', 'slug': 'hackathon', 'color': 'red', 'icon': 'code'},
    ]

    cats = {}
    for cat_data in categories:
        cat, created = EventCategory.objects.get_or_create(
            slug=cat_data['slug'],
            defaults=cat_data
        )
        cats[cat.slug] = cat
        print(f"{'Created' if created else 'Existing'} category: {cat.name}")

    # Create Events
    now = timezone.now()
    
    events_data = [
        {
            'title': 'Python for Beginners Workshop',
            'slug': 'python-for-beginners-workshop-2025',
            'category': cats['workshop'],
            'description': '''
Join us for an intensive hands-on workshop designed to get you started with Python programming. 
We will cover the basics of syntax, data structures, and control flow. No prior experience required!

What you will learn:
- Installing Python and VS Code
- Variables and Data Types
- Lists, Dictionaries, and Sets
- Loops and Conditionals
- Basic Functions
            ''',
            'short_description': 'Learn the basics of Python programming in this hands-on workshop. Perfect for absolute beginners.',
            'event_type': 'online',
            'online_link': 'https://meet.google.com/abc-defg-hij',
            'start_datetime': now + timedelta(days=7),
            'end_datetime': now + timedelta(days=7, hours=3),
            'max_attendees': 50,
            'organizer': admin_user,
            'status': 'published',
            'is_featured': True,
            'is_free': True,
            'tags': 'python, beginners, coding',
        },
        {
            'title': 'Vientiane Python Meetup: AI & Machine Learning',
            'slug': 'vientiane-python-meetup-ai-ml',
            'category': cats['meetup'],
            'description': '''
Let's gather to discuss the latest trends in AI and Machine Learning. 
We'll have two guest speakers from the industry sharing their experiences.
Pizza and drinks will be provided!
            ''',
            'short_description': 'Monthly meetup for Python enthusiasts in Vientiane. This month\'s topic: AI & Machine Learning.',
            'event_type': 'offline',
            'venue': 'Phenomenal Office, Vientiane Center',
            'venue_address': '4th Floor, Vientiane Center, Khouvieng Road, Vientiane',
            'start_datetime': now + timedelta(days=14, hours=10),
            'end_datetime': now + timedelta(days=14, hours=13),
            'max_attendees': 30,
            'organizer': admin_user,
            'status': 'published',
            'is_featured': False,
            'is_free': False,
            'price': 50000,
            'tags': 'ai, machine learning, networking',
        },
        {
            'title': 'Django Web Development Bootcamp',
            'slug': 'django-bootcamp-2025',
            'category': cats['workshop'],
            'description': '''
Build your first web application with Django! 
This is a comprehensive bootcamp where we will build a blog application from scratch.
Prerequisites: Basic Python knowledge.
            ''',
            'short_description': 'A full-day bootcamp to learn Django web framework. Build a real-world project.',
            'event_type': 'hybrid',
            'venue': 'National University of Laos',
            'venue_address': 'Dongdok Campus, Vientiane',
            'online_link': 'https://zoom.us/j/123456789',
            'start_datetime': now + timedelta(days=30),
            'end_datetime': now + timedelta(days=30, hours=6),
            'max_attendees': 100,
            'organizer': admin_user,
            'status': 'published',
            'is_featured': True,
            'is_free': False,
            'price': 150000,
            'tags': 'django, web, backend',
        },
        {
            'title': 'Lao Python Conference 2024 (Past Event)',
            'slug': 'lao-python-conf-2024',
            'category': cats['conference'],
            'description': '''
The biggest Python event in Laos. 
Thank you specifically to all our sponsors and speakers.
See you next year!
            ''',
            'short_description': 'Annual gathering of Python developers in Laos.',
            'event_type': 'offline',
            'venue': 'Lao Plaza Hotel',
            'venue_address': 'Vientiane',
            'start_datetime': now - timedelta(days=60),
            'end_datetime': now - timedelta(days=60, hours=8),
            'max_attendees': 200,
            'organizer': admin_user,
            'status': 'completed',
            'is_featured': False,
            'is_free': False,
            'price': 250000,
            'tags': 'conference, community',
        }
    ]

    for event_data in events_data:
        event, created = Event.objects.get_or_create(
            slug=event_data['slug'],
            defaults=event_data
        )
        print(f"{'Created' if created else 'Existing'} event: {event.title}")

if __name__ == '__main__':
    populate()
