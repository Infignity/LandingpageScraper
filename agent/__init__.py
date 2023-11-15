import os
import sys
from celery import Celery


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)


def route_task(name, args, kwargs, options, task=None, **kw):
    if ":" in name:
        _, queue = name.split(":")
        return {"queue": queue}
    return {"queue": "celery"}


celery_app = Celery(
    __name__,
    include=["tasks"],
)

celery_app.config_from_object('celeryconfig')
celery_app.conf.task_default_queue = "celery"
celery_app.conf.task_routes = (route_task,)
celery_app.autodiscover_tasks()
