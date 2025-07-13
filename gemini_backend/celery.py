import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gemini_backend.settings')

app = Celery('gemini_backend')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Configure Celery for production with Render Redis
app.conf.update(
    broker_connection_retry_on_startup=True,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    broker_connection_retry=True,
    broker_connection_max_retries=10,
)

app.autodiscover_tasks() 