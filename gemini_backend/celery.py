import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gemini_backend.settings')

app = Celery('gemini_backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks() 