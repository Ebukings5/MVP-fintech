from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance_manager.settings')

app = Celery('finance_manager')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover tasks in installed apps
app.autodiscover_tasks()

# Optional: Define a task name prefix
app.conf.task_name_prefix = 'finance_manager.'

# Optional: Configure result backend (if needed)
# Use Django's database as the result backend
app.conf.result_backend = 'django-db'

# Optional: Configure the task serializer and result serializer
app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'
app.conf.accept_content = ['json']

# Optional: Configure time zone for Celery
app.conf.timezone = 'UTC'

# Optional: Configure Celery to use a custom timezone-aware datetime object
app.conf.enable_utc = True

# Optional: Configure Celery to use a specific task queue
app.conf.task_queues = {
    'default': {
        'exchange': 'default',
        'routing_key': 'default'
    },
    'high_priority': {
        'exchange': 'high_priority',
        'routing_key': 'high_priority'
    },
}

# Optional: Configure periodic tasks (if needed)
from celery.schedules import crontab

app.conf.beat_schedule = {
    'send_daily_reports': {
        'task': 'your_app.tasks.send_daily_reports',
        'schedule': crontab(hour=0, minute=0),
        'args': (),
    },
}

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
