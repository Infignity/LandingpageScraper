from src.agent import celery_app
from typing import List
from celery.result import AsyncResult


@celery_app.task(name="run_crawler")
def crawler_task(
    tracking_id: str,
    urls: List[str]
):
    """ Crawler function """
    
    return {"urls": urls, "tracking_id": tracking_id}
    
