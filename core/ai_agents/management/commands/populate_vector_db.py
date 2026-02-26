"""
Django Management Command to Populate Vector Database
ຄຳສັ່ງເພີ່ມຂໍ້ມູນເຂົ້າ Vector Database
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from ai_agents.tasks import populate_vector_database_task


class Command(BaseCommand):
    help = 'Populate vector database with all content (posts, courses, docs)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--async',
            action='store_true',
            help='Run as async Celery task',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Starting vector database population...'))

        if options['async']:
            # Run as Celery task
            task = populate_vector_database_task.delay()
            self.stdout.write(
                self.style.SUCCESS(f'Task queued with ID: {task.id}')
            )
            self.stdout.write(
                'Run "celery -A core worker" to process the task'
            )
        else:
            # Run synchronously
            result = populate_vector_database_task()

            if result.get('status') == 'success':
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully populated vector database!\n"
                        f"Total documents: {result.get('total_documents')}\n"
                        f"Blog posts: {result.get('posts')}\n"
                        f"Courses: {result.get('courses')}\n"
                        f"Documentation: {result.get('docs')}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f"Error: {result.get('error')}")
                )
