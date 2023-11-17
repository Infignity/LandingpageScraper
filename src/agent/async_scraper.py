import asyncio
import httpx
from selectolax.parser import HTMLParser
from src.database import init_db
from src.models import Task
from src.app_config import get_random_ua
from beanie import PydanticObjectId


async def send_until_ok(session: httpx.AsyncClient,url, random_ua=get_random_ua()) -> HTMLParser:
    try:
        resp = await session.get(url, headers={"user-agent": random_ua}):
        if resp.status  in in [200]:
            return HTMLParser(resp.content)

    except (
        httpx.Client
        UnicodeEncodeError
    ) as err:
        pass
        # print(f"Error : {err}")

    print(f"Retrying -> {url}")
    return await send_until_ok(client, url, random_proxy)

async def scrape_url(session: httpx.AsyncClient, url: str, task_id: PydanticObjectId):
    task = await Task.get(task_id)
    task.scraped_urls.add(url)
    task.results = [{"s":"somethingchangesd"}]
    await task.save_changes()

async def update_task_state(task_id, state):
    task = await Task.get(task_id)
    if task:
        task.state = state
        await task.save_changes()

async def run(task_id_str, urls, start_n:int = 0):
    total_urls = len(urls)
    task_id = PydanticObjectId(task_id_str)
    
    print(f"Starting task -> {task_id_str} -> {total_urls} urls")
    
    await init_db([Task])
    await update_task_state(task_id, "running")
    
    chunk_size = 10
    
    async with httpx.AsyncClient() as session:
        for i in range(start_n, total_urls, chunk_size):
            scraped_urls = set()
            task = await Task.get(task_id)
            if task is not None:
                scraped_urls = task.scraped_urls
            
            batch = set(urls[i:i+chunk_size]).difference(scraped_urls)
            print(f"Scraping batch [{task_id_str}] -> {i}-{i+chunk_size} {len(batch)}")
            tasks = [scrape_url(session, url, task_id) for url in batch]
            await asyncio.gather(*tasks)
    
    await update_task_state(task_id, "completed")
        