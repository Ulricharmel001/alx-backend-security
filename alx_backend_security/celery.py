import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_security.settings')

app = Celery('alx_backend_security')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Configure periodic tasks
app.conf.beat_schedule = {
    'detect-anomalous-ips-hourly': {
        'task': 'ip_tracking.tasks.detect_anomalous_ips',
        'schedule': crontab(minute=0),  # Run every hour at minute 0
    },
}

app.conf.timezone = 'Africa/Lagos'