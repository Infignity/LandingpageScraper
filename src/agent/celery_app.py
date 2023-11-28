from celery import Celery
from src.agent import celeryconfig

app = Celery('celery_tasks')
app.config_from_object(celeryconfig)
app.autodiscover_tasks()
