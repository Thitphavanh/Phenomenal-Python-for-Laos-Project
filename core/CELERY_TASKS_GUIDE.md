# Celery Tasks Guide - AI Agents
# ຄູ່ມືການໃຊ້ງານ Celery Tasks ສຳລັບ AI Agents

## Overview / ພາບລວມ

Celery tasks are used for asynchronous processing of long-running operations in the AI Agents system. This includes analytics generation, payment slip processing, recommendations, and vector database management.

**Celery tasks** ຖືກໃຊ້ສຳລັບການປະມວນຜົນແບບ asynchronous ສຳລັບການດຳເນີນງານທີ່ໃຊ້ເວລາດົນໃນລະບົບ AI Agents.

---

## Installation & Setup / ການຕິດຕັ້ງແລະຕັ້ງຄ່າ

### 1. Install Dependencies

```bash
cd core
pip install -r requirements.txt
```

### 2. Install and Run Redis

**On macOS:**
```bash
brew install redis
brew services start redis
```

**On Ubuntu/Debian:**
```bash
sudo apt-get install redis-server
sudo systemctl start redis
sudo systemctl enable redis
```

**Verify Redis is running:**
```bash
redis-cli ping
# Should return: PONG
```

### 3. Environment Configuration

Make sure your `.env` file includes:

```env
# Redis & Celery Configuration
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0
```

### 4. Run Database Migrations

```bash
python manage.py migrate
```

This will create tables for:
- `django_celery_beat` - Periodic task scheduler
- `django_celery_results` - Task results storage

---

## Running Celery / ການເປີດໃຊ້ງານ Celery

### Start Celery Worker

Open a new terminal and run:

```bash
cd core
celery -A core worker --loglevel=info
```

**With multiple queues:**
```bash
celery -A core worker -Q default,analytics,payment,recommendations,vector_db --loglevel=info
```

### Start Celery Beat (Periodic Tasks)

Open another terminal and run:

```bash
cd core
celery -A core beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

### Monitor Tasks with Flower (Optional)

```bash
pip install flower
celery -A core flower
```

Then visit: http://localhost:5555

---

## Available Tasks / Task ທີ່ມີ

### 1. Analytics Tasks

#### Generate Course Analytics
```python
from ai_agents.tasks import generate_course_analytics_task

# Run async
task = generate_course_analytics_task.delay(course_id=1)
print(f"Task ID: {task.id}")

# Check result
result = task.get()
```

**Django Shell Example:**
```bash
python manage.py shell
```
```python
from ai_agents.tasks import generate_course_analytics_task

# Queue task
task = generate_course_analytics_task.delay(1)

# Wait for result
result = task.get(timeout=300)  # 5 minutes timeout
print(result)
```

#### Generate All Courses Analytics
```python
from ai_agents.tasks import generate_all_courses_analytics_task

task = generate_all_courses_analytics_task.delay()
```

#### Generate Monthly BI Report
```python
from ai_agents.tasks import generate_monthly_bi_report_task

task = generate_monthly_bi_report_task.delay()
result = task.get()
```

---

### 2. Payment Slip Processing Tasks

#### Process Single Payment Slip
```python
from ai_agents.tasks import process_payment_slip_task

# After uploading payment slip via API
task = process_payment_slip_task.delay(analysis_id=1)
```

#### Process All Pending Payment Slips
```python
from ai_agents.tasks import process_pending_payment_slips_task

task = process_pending_payment_slips_task.delay()
```

---

### 3. Recommendation Tasks

#### Generate User Recommendations
```python
from ai_agents.tasks import generate_user_recommendations_task

task = generate_user_recommendations_task.delay(user_id=1, limit=5)
result = task.get()
```

#### Generate All Users Recommendations
```python
from ai_agents.tasks import generate_all_users_recommendations_task

task = generate_all_users_recommendations_task.delay()
```

---

### 4. Vector Database Tasks

#### Populate Vector Database
```python
from ai_agents.tasks import populate_vector_database_task

task = populate_vector_database_task.delay()
result = task.get(timeout=600)  # 10 minutes
```

**Or use management command:**
```bash
# Synchronous
python manage.py populate_vector_db

# Asynchronous
python manage.py populate_vector_db --async
```

#### Update Single Document
```python
from ai_agents.tasks import update_vector_document_task

# Update blog post
task = update_vector_document_task.delay('blog_post', 1)

# Update course
task = update_vector_document_task.delay('course', 1)

# Update documentation
task = update_vector_document_task.delay('documentation', 1)
```

---

### 5. Maintenance Tasks

#### Cleanup Old Analytics
```python
from ai_agents.tasks import cleanup_old_analytics_task

# Keep only last 30 days
task = cleanup_old_analytics_task.delay(days=30)
```

---

## Periodic Tasks / Task ປະຈຳ

The system includes automatic periodic tasks configured in Celery Beat:

### Daily Tasks (2 AM)
- Generate recommendations for all users
- Generate analytics for all courses
- Process pending payment slips

### Weekly Tasks (3 AM Sunday)
- Cleanup old analytics (30 days)
- Rebuild vector database

### Monthly Tasks (4 AM, 1st of month)
- Generate Business Intelligence report

### Custom Schedules
- **Every 6 hours**: Generate all course analytics
- **Every hour**: Process pending payment slips

---

## Task Queues / ຄິວ Task

The system uses multiple queues for better organization:

| Queue | Purpose | Tasks |
|-------|---------|-------|
| `default` | General tasks | Daily/weekly/monthly tasks |
| `analytics` | Analytics generation | Course analytics, BI reports |
| `payment` | Payment processing | Payment slip OCR & analysis |
| `recommendations` | Recommendations | Course recommendations |
| `vector_db` | Vector DB operations | Populate, update documents |

**Start worker with specific queues:**
```bash
# Only analytics queue
celery -A core worker -Q analytics --loglevel=info

# Multiple queues
celery -A core worker -Q analytics,payment --loglevel=info
```

---

## Monitoring & Debugging / ການຕິດຕາມແລະແກ້ໄຂບັນຫາ

### Check Task Status

```python
from celery.result import AsyncResult

task_id = "your-task-id-here"
result = AsyncResult(task_id)

print(f"Status: {result.status}")
print(f"Result: {result.result}")
print(f"Ready: {result.ready()}")
print(f"Successful: {result.successful()}")
```

### View Logs

Celery worker logs show:
- Task started
- Task progress
- Task completed/failed
- Errors and exceptions

```bash
# Worker terminal shows:
[2024-01-11 10:30:00,000: INFO/MainProcess] Received task: ai_agents.tasks.generate_course_analytics_task[task-id]
[2024-01-11 10:30:05,000: INFO/ForkPoolWorker-1] Task ai_agents.tasks.generate_course_analytics_task[task-id] succeeded
```

### Django Admin

Visit Django admin to manage periodic tasks:
- **Periodic Tasks**: Configure scheduled tasks
- **Crontab Schedules**: Manage cron schedules
- **Intervals**: Manage interval schedules

**URL:** http://localhost:8000/admin/django_celery_beat/

---

## Error Handling / ການຈັດການຄວາມຜິດພາດ

Tasks automatically retry on failure:

- **Max retries**: 3
- **Retry countdown**: Exponential backoff (2^retry_count seconds)

```python
@shared_task(bind=True, max_retries=3)
def my_task(self):
    try:
        # Task logic
        pass
    except Exception as e:
        # Retry with exponential backoff
        raise self.retry(exc=e, countdown=2 ** self.request.retries)
```

### Manual Retry

```python
from celery import current_app

# Retry specific task
task_id = "failed-task-id"
current_app.send_task('ai_agents.tasks.generate_course_analytics_task', args=[1])
```

---

## Production Deployment / ການນຳໃຊ້ໃນ Production

### Using Supervisor (Recommended)

Install Supervisor:
```bash
sudo apt-get install supervisor
```

Create config file `/etc/supervisor/conf.d/celery.conf`:

```ini
[program:celery_worker]
command=/path/to/venv/bin/celery -A core worker --loglevel=info -Q default,analytics,payment,recommendations,vector_db
directory=/path/to/core
user=www-data
numprocs=1
stdout_logfile=/var/log/celery/worker.log
stderr_logfile=/var/log/celery/worker_error.log
autostart=true
autorestart=true
startsecs=10
stopwaitsecs=600

[program:celery_beat]
command=/path/to/venv/bin/celery -A core beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
directory=/path/to/core
user=www-data
numprocs=1
stdout_logfile=/var/log/celery/beat.log
stderr_logfile=/var/log/celery/beat_error.log
autostart=true
autorestart=true
startsecs=10
```

Create log directory:
```bash
sudo mkdir -p /var/log/celery
sudo chown www-data:www-data /var/log/celery
```

Start services:
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start celery_worker
sudo supervisorctl start celery_beat
```

### Using Systemd

Create `/etc/systemd/system/celery.service`:

```ini
[Unit]
Description=Celery Service
After=network.target redis.service

[Service]
Type=forking
User=www-data
Group=www-data
WorkingDirectory=/path/to/core
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/celery -A core worker --loglevel=info -Q default,analytics,payment,recommendations,vector_db --detach

[Install]
WantedBy=multi-user.target
```

Create `/etc/systemd/system/celerybeat.service`:

```ini
[Unit]
Description=Celery Beat Service
After=network.target redis.service

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/path/to/core
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/celery -A core beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler

[Install]
WantedBy=multi-user.target
```

Start services:
```bash
sudo systemctl daemon-reload
sudo systemctl start celery
sudo systemctl start celerybeat
sudo systemctl enable celery
sudo systemctl enable celerybeat
```

---

## Common Use Cases / ກໍລະນີການໃຊ້ງານທົ່ວໄປ

### 1. After Creating New Content

When a new blog post, course, or documentation is created:

```python
from ai_agents.tasks import update_vector_document_task

# Add to vector database
update_vector_document_task.delay('blog_post', post.id)
```

### 2. After User Enrolls in Course

Generate new recommendations:

```python
from ai_agents.tasks import generate_user_recommendations_task

# User just enrolled in a course, update recommendations
generate_user_recommendations_task.delay(user.id)
```

### 3. Payment Slip Upload

Process payment slip asynchronously:

```python
from ai_agents.tasks import process_payment_slip_task

# After user uploads payment slip
analysis = PaymentSlipAnalysis.objects.create(image=uploaded_file, user=user)
process_payment_slip_task.delay(analysis.id)
```

### 4. Weekly Analytics Report

Schedule weekly analytics:

```python
from django_celery_beat.models import PeriodicTask, CrontabSchedule

# Create schedule (Every Monday 9 AM)
schedule, _ = CrontabSchedule.objects.get_or_create(
    minute='0',
    hour='9',
    day_of_week='1',
)

# Create task
PeriodicTask.objects.create(
    crontab=schedule,
    name='Weekly Analytics Report',
    task='ai_agents.tasks.generate_all_courses_analytics_task',
)
```

---

## Testing / ການທົດສອບ

### Test Tasks Locally

```python
# test_tasks.py
from django.test import TestCase
from ai_agents.tasks import generate_course_analytics_task
from courses.models import Course

class TaskTests(TestCase):
    def test_generate_analytics(self):
        course = Course.objects.create(title="Test Course")

        # Run task synchronously
        result = generate_course_analytics_task(course.id)

        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['course_id'], course.id)
```

Run tests:
```bash
python manage.py test ai_agents.tests.test_tasks
```

---

## Troubleshooting / ການແກ້ໄຂບັນຫາ

### Redis Connection Error

```
Error: Error 111 connecting to localhost:6379. Connection refused.
```

**Solution:**
```bash
# Start Redis
brew services start redis  # macOS
sudo systemctl start redis  # Linux
```

### Task Not Processing

**Check:**
1. Is Celery worker running?
2. Is Redis running?
3. Check worker logs for errors
4. Verify task is queued: `redis-cli LLEN celery`

### Import Errors

```
ImportError: No module named 'ai_agents.tasks'
```

**Solution:**
```bash
# Make sure DJANGO_SETTINGS_MODULE is set
export DJANGO_SETTINGS_MODULE=core.settings.dev

# Restart Celery worker
```

### Task Timeout

Increase time limits in settings:

```python
# settings/base.py
CELERY_TASK_TIME_LIMIT = 60 * 60  # 1 hour
CELERY_TASK_SOFT_TIME_LIMIT = 55 * 60  # 55 minutes
```

---

## Performance Optimization / ການເພີ່ມປະສິດທິພາບ

### 1. Increase Worker Concurrency

```bash
celery -A core worker --concurrency=4
```

### 2. Use Prefetch Limit

```python
# settings/base.py
CELERY_WORKER_PREFETCH_MULTIPLIER = 1  # Process one task at a time
```

### 3. Set Task Priorities

```python
task = generate_course_analytics_task.apply_async(
    args=[course_id],
    priority=10  # Higher priority
)
```

### 4. Enable Task Compression

```python
# settings/base.py
CELERY_TASK_COMPRESSION = 'gzip'
```

---

## Resources / ແຫຼ່ງຂໍ້ມູນ

- **Celery Documentation**: https://docs.celeryq.dev/
- **Django Celery Beat**: https://django-celery-beat.readthedocs.io/
- **Redis Documentation**: https://redis.io/documentation
- **Flower Monitoring**: https://flower.readthedocs.io/

---

## Summary / ສະຫຼຸບ

This guide covers:
- ✅ Installation and setup
- ✅ Running Celery worker and beat
- ✅ All available tasks
- ✅ Periodic task scheduling
- ✅ Queue management
- ✅ Monitoring and debugging
- ✅ Production deployment
- ✅ Common use cases
- ✅ Troubleshooting

**Next Steps:**
1. Install Redis and Celery dependencies
2. Run migrations
3. Start Celery worker and beat
4. Test tasks in Django shell
5. Configure periodic tasks in admin
6. Deploy to production with Supervisor or Systemd

---

**ສຳເລັດແລ້ວ! Your Celery tasks are ready to use.**
