from django.core.management.base import BaseCommand
from ai_agents.services.vector_db import VectorDBService
from ai_agents.utils.helpers import truncate_text
from courses.models import Course, Lesson
from blog.models import Post
from community.models import Topic
from docs.models import Documentation
from events.models import Event
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Index content into Vector DB for AI Agents'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clean',
            action='store_true',
            help='Delete existing collection before indexing',
        )

    def handle(self, *args, **options):
        vdb = VectorDBService()

        if options['clean']:
            self.stdout.write('Cleaning existing collection...')
            vdb.delete_collection()
            # Re-initialize to create fresh collection
            vdb = VectorDBService()

        self.stdout.write('Indexing Courses...')
        courses = Course.objects.all()
        course_docs = []

        for course in courses:
            # Index Course Description
            text = f"Course: {course.title}\nDescription: {course.short_description}\n\n{course.description}"
            course_docs.append({
                'id': f"course_{course.id}",
                'text': text,
                'metadata': {
                    'source': 'course',
                    'title': course.title,
                    'course_id': course.id,
                    'url': f"/courses/{course.slug}/"
                }
            })
            
            # Index Lessons
            lessons = Lesson.objects.filter(course=course)
            self.stdout.write(f"  - Found {lessons.count()} lessons for {course.title}")
            
            for lesson in lessons:
                 # Truncate content to avoid token limits (approx 8000 chars ~ 2000 tokens)
                 content_extract = truncate_text(lesson.content, max_tokens=2000)
                 text = f"Course: {course.title}\nLesson: {lesson.title}\n\n{content_extract}"
                 
                 course_docs.append({
                    'id': f"lesson_{lesson.id}",
                    'text': text,
                    'metadata': {
                        'source': 'lesson',
                        'title': lesson.title,
                        'course_id': course.id,
                        'lesson_id': lesson.id,
                        'url': f"/courses/{course.slug}/lessons/{lesson.pk}/"
                    }
                 })

        self.stdout.write('Indexing Blog & Community Posts...')
        posts = Post.objects.filter(status='published')
        blog_docs = []
        for post in posts:
            content_extract = truncate_text(post.content, max_tokens=2000)
            text = f"{post.get_post_type_display()}: {post.title}\nExcerpt: {post.excerpt}\n\n{content_extract}"
            blog_docs.append({
                'id': f"post_{post.id}",
                'text': text,
                'metadata': {
                    'source': post.post_type,
                    'title': post.title,
                    'url': post.get_absolute_url()
                }
            })

        self.stdout.write('Indexing Community Topics...')
        topics = Topic.objects.all()
        topic_docs = []
        for topic in topics:
            text = f"Community Topic: {topic.title}\n\n{topic.content}"
            topic_docs.append({
                'id': f"topic_{topic.id}",
                'text': text,
                'metadata': {
                    'source': 'community',
                    'title': topic.title,
                    'url': topic.get_absolute_url()
                }
            })

        self.stdout.write('Indexing Documentation...')
        docs = Documentation.objects.filter(status='published')
        doc_entries = []
        for doc in docs:
            content_extract = truncate_text(doc.content, max_tokens=2000)
            text = f"Documentation: {doc.title}\nCategory: {doc.category.name if doc.category else 'General'}\n\n{content_extract}"
            doc_entries.append({
                'id': f"doc_{doc.id}",
                'text': text,
                'metadata': {
                    'source': 'docs',
                    'title': doc.title,
                    'url': doc.get_absolute_url()
                }
            })

        self.stdout.write('Indexing Events...')
        events = Event.objects.filter(status='published')
        event_docs = []
        for event in events:
            text = f"Event: {event.title}\nType: {event.get_event_type_display()}\nDate: {event.start_datetime.strftime('%Y-%m-%d')}\nVenue: {event.venue}\n\n{event.description}"
            event_docs.append({
                'id': f"event_{event.id}",
                'text': text,
                'metadata': {
                    'source': 'event',
                    'title': event.title,
                    'url': event.get_absolute_url()
                }
            })

        all_docs = course_docs + blog_docs + topic_docs + doc_entries + event_docs

        if all_docs:
            self.stdout.write(f'Adding {len(all_docs)} documents to Vector DB...')
            success = vdb.add_documents(all_docs)
            if success:
                self.stdout.write(self.style.SUCCESS('Successfully indexed content'))
            else:
                self.stdout.write(self.style.ERROR('Failed to index content'))
        else:
             self.stdout.write('No content found to index.')
