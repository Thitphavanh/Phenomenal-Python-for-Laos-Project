"""
Celery Configuration for Core Project
ການຕັ້ງຄ່າ Celery ສຳລັບ Project
"""

import os
from celery import Celery
from celery.schedules import crontab

# Set default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')

# Create Celery app
app = Celery('core')

# Load config from Django settings with 'CELERY_' prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all installed apps
app.autodiscover_tasks()


# Celery Beat Schedule for Periodic Tasks
app.conf.beat_schedule = {
    # Daily tasks - Run at 2 AM every day
    'daily-maintenance': {
        'task': 'ai_agents.tasks.daily_tasks',
        'schedule': crontab(hour=2, minute=0),
        'options': {'queue': 'default'}
    },

    # Weekly tasks - Run at 3 AM every Sunday
    'weekly-maintenance': {
        'task': 'ai_agents.tasks.weekly_tasks',
        'schedule': crontab(hour=3, minute=0, day_of_week=0),
        'options': {'queue': 'default'}
    },

    # Monthly tasks - Run at 4 AM on 1st of every month
    'monthly-maintenance': {
        'task': 'ai_agents.tasks.monthly_tasks',
        'schedule': crontab(hour=4, minute=0, day_of_month=1),
        'options': {'queue': 'default'}
    },

    # Generate all course analytics - Every 6 hours
    'generate-all-analytics': {
        'task': 'ai_agents.tasks.generate_all_courses_analytics_task',
        'schedule': crontab(minute=0, hour='*/6'),
        'options': {'queue': 'analytics'}
    },

    # Process pending payment slips - Every hour
    'process-pending-payments': {
        'task': 'ai_agents.tasks.process_pending_payment_slips_task',
        'schedule': crontab(minute=0),
        'options': {'queue': 'payment'}
    },
}


# Celery Task Routes
app.conf.task_routes = {
    'ai_agents.tasks.generate_course_analytics_task': {'queue': 'analytics'},
    'ai_agents.tasks.generate_all_courses_analytics_task': {'queue': 'analytics'},
    'ai_agents.tasks.generate_monthly_bi_report_task': {'queue': 'analytics'},
    'ai_agents.tasks.process_payment_slip_task': {'queue': 'payment'},
    'ai_agents.tasks.process_pending_payment_slips_task': {'queue': 'payment'},
    'ai_agents.tasks.generate_user_recommendations_task': {'queue': 'recommendations'},
    'ai_agents.tasks.generate_all_users_recommendations_task': {'queue': 'recommendations'},
    'ai_agents.tasks.populate_vector_database_task': {'queue': 'vector_db'},
    'ai_agents.tasks.update_vector_document_task': {'queue': 'vector_db'},
}


@app.task(bind=True)
def debug_task(self):
    """Debug task for testing Celery"""
    print(f'Request: {self.request!r}')
