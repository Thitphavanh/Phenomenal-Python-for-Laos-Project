import os
import django
import random

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.dev')
django.setup()

from django.contrib.auth.models import User
from blog.models import Category
from community.models import Topic, Reply

def populate():
    print("Populating community data...")

    # Get or create a superuser or standard user
    user, created = User.objects.get_or_create(username='admin')
    if created:
        user.set_password('admin')
        user.save()
        print("Created admin user.")
    
    # Get categories
    categories = list(Category.objects.all())
    if not categories:
        print("No categories found. Please create categories first.")
        # Create dummy categories if none exist
        Category.objects.get_or_create(name='Python', slug='python')
        Category.objects.get_or_create(name='Django', slug='django')
        Category.objects.get_or_create(name='General', slug='general')
        categories = list(Category.objects.all())

    # Sample Topics
    topics_data = [
        {
            "title": "How to start with Python?",
            "content": "I am a beginner and I want to learn Python. What are the best resources for a complete newbie in Laos? looking for free tutorials.",
            "category": "python",
            "solved": True
        },
        {
            "title": "Django vs Flask for a small project",
            "content": "I'm building a simple personal blog. Should I use Django or Flask? I know Django has batteries included but Flask seems simpler.",
            "category": "django",
            "solved": False
        },
        {
            "title": "Where can I find Python jobs in Vientiane?",
            "content": "Are there many companies hiring Python developers in Laos? What skills are they looking for besides basic syntax?",
            "category": "general",
            "solved": False
        },
        {
            "title": "Error installing Pillow on Mac",
            "content": "I keep getting an error when running `pip install Pillow`. Something about zlib missing. Has anyone faced this?",
            "category": "python",
            "solved": True
        },
        {
            "title": "Best way to deploy Django on a VPS",
            "content": "I have a DigitalOcean droplet. What is the recommended stack? Gunicorn + Nginx? Docker?",
            "category": "django",
            "solved": False
        }
    ]

    for data in topics_data:
        # Find category by slug/name match
        cat_obj = next((c for c in categories if data['category'].lower() in c.slug or data['category'].lower() in c.name.lower()), categories[0])
        
        topic, created = Topic.objects.get_or_create(
            title=data['title'],
            defaults={
                'content': data['content'],
                'author': user,
                'category': cat_obj,
                'is_solved': data['solved']
            }
        )
        
        if created:
            print(f"Created topic: {topic.title}")
            
            # Create replies
            num_replies = random.randint(1, 4)
            for i in range(num_replies):
                Reply.objects.create(
                    topic=topic,
                    author=user,
                    content=f"This is a sample reply #{i+1}. Hopefully this helps you with your question about {topic.title}.",
                    is_accepted_answer=(i == 0 and data['solved'])
                )
            print(f"  - Added {num_replies} replies.")
        else:
            print(f"Topic already exists: {topic.title}")

    print("Done!")

if __name__ == '__main__':
    populate()
