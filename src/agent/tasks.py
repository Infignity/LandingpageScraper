from src.agent import celery_app
from typing import List
from celery.result import AsyncResult
from src.agent.async_scraper import run
import asyncio

@celery_app.task(name="run_crawler")
def crawler_task(
    task_id_str: str,
    urls: List[str]
):
    """ Crawler function """
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(task_id_str, urls))
    
    return f"Task with id={task_id_str} has been completed !"
    
