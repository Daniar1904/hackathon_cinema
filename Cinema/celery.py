import os
from celery import Celery

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'Cinema.settings'
)

app = Celery('Cinema')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
