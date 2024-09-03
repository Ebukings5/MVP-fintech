from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

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
# app.conf.result_backend = 'your_backend_url'