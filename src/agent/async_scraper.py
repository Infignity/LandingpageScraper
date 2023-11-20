import asyncio
import httpx
import ssl
import anyio
from selectolax.parser import HTMLParser
from src.database import init_db
from src.models import Task, TaskResult
from src.app_config import get_random_ua
from src.utils import strip_text
from beanie import PydanticObjectId
from src.exceptions import MaxretriesError, EmptyParserError, InvalidUrlError

MAX_RETRIES = 3


async def send_until_ok(session: httpx.AsyncClient,url, random_ua=get_random_ua(), retries=0) -> HTMLParser:
    if not isinstance(url, str):
        print(f"URL TYPE {type(str)}")
        raise InvalidUrlError(f"Invalid Url")
    
    try:
        resp = await session.get(url, headers={"user-agent": random_ua}, follow_redirects=True)
        if resp.status_code in [200, 301, 302]:
            return HTMLParser(resp.content)
    
    except (TypeError, ssl.SSLCertVerificationError) as e:
        raise InvalidUrlError(f"Invalid Url")

    except (
        httpx.ReadTimeout,
        httpx.ReadError,
        UnicodeEncodeError,
        httpx.ConnectError,
        httpx.ConnectTimeout,
        httpx.RemoteProtocolError,
        httpx.PoolTimeout,
        TimeoutError,
        anyio.EndOfStream
    ) as e:
        pass
    
    if retries > MAX_RETRIES:
        raise MaxretriesError("Max retries reached")
    
    print(f"Retrying -> {url}")
    return await send_until_ok(session, url, retries=retries+1)

def format_url(url):
    f_url = url
    if not url.startswith("https") and not url.startswith("http"):
        f_url = f"https://{url}"
    return f_url

async def scrape_url(session: httpx.AsyncClient, url: str, task_id: PydanticObjectId):
    if isinstance(url, str):
        url  = format_url(url)
        task = await Task.get(task_id)
        
        try:
            parser = await send_until_ok(session, url)
            p_tags = parser.css('p')
            texts = [p.text(strip=True) for p in p_tags]
            landing_page_text = (".".join(texts)).replace("..",".")

            new_task_result = TaskResult(landing_page_text=landing_page_text, task_id=task_id, url=url)
            await new_task_result.create()
            
        except (InvalidUrlError, MaxretriesError):
            pass
        

async def update_task_state(task_id, state):
    task = await Task.get(task_id)
    if task:
        task.state = state
        await task.save_changes()

async def run(task_id_str, urls, start_n:int = 0):
    total_urls = len(urls)
    task_id = PydanticObjectId(task_id_str)
    
    print(f"Starting task -> {task_id_str} -> {total_urls} urls")
    
    await init_db([Task, TaskResult])
    
    # await Task.delete_all()
    # await TaskResult.delete_all()
    
    await update_task_state(task_id, "running")
    
    chunk_size = 150
    
    async with httpx.AsyncClient(timeout=30, follow_redirects=True) as session:
        for i in range(start_n, total_urls, chunk_size):
            scraped_urls = set()
            task = await Task.get(task_id)
            if task is not None:
                scraped_urls = set(task.scraped_urls)
            
            batch = set(urls[i:i+chunk_size]).difference(scraped_urls)
            print(f"Scraping batch [{task_id_str}] -> {i}-{i+chunk_size} {len(batch)}")
            tasks = [scrape_url(session, url, task_id) for url in batch]
            await asyncio.gather(*tasks)
            
    task = await Task.get(task_id)
    task_results = await TaskResult.find(TaskResult.task_id ==  task_id).to_list()
    task.results = task_results
    task.state = "completed"
    await task.save_changes()
