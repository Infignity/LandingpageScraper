'''lib import'''
import uuid
from io import BytesIO
from fastapi import (
    APIRouter, 
    Request, 
    status,  
    Response,
    UploadFile, File, HTTPException)
import os  
from fastapi.responses import JSONResponse
from starlette.templating import Jinja2Templates
from src.models import Task
from src.agent.tasks import crawler_task
from src.app_config import BASE_DIR
from src import read_csv_file
from src.schemas import TaskView

router = APIRouter()
jin_template = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


@router.get("/")
async def get_tasks(
    request: Request,
    response: Response
):
    """ Get form page and results """
    
    tasks = await Task.find().project(TaskView).to_list()
    print("TASKS: ",tasks)
    context = {"request": request, "data": []}
    
    response.status_code = status.HTTP_200_OK
    return jin_template.TemplateResponse("index.html", context)


@router.post('/scrape')
async def add_task(
    request: Request, 
    response: Response,
    file: UploadFile = File(...)
):
    """ Register new scraping task """
    
    urls = []
    try:
        csv_bytes = file.file.read()
        buffer = BytesIO(csv_bytes)
        urls = read_csv_file(buffer, 'organization_website')
    except:
        raise HTTPException(status_code=500, detail='Something went wrong')
    finally:
        # closing both the file and the buffer 
        buffer.close()
        file.file.close()

    new_task = Task()
    
    # call task multiple time to ensure success
    task_result = crawler_task.delay(
        str(new_task.id),
        urls,
    )
    
    new_task.celery_task_id = task_result.id
    await new_task.create()
    
    response.status_code = status.HTTP_200_OK
 
    return new_task.model_dump(exclude=["results", "scraped_urls"])
    

