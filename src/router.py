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
from fastapi.responses import JSONResponse, StreamingResponse
from starlette.templating import Jinja2Templates
from src.models import Task, TaskResult
from src.agent.tasks import crawler_task
from src.app_config import BASE_DIR
from src import read_csv_file
from src.schemas import TaskView
import pandas as pd
from beanie import PydanticObjectId

router = APIRouter()
jin_template = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


@router.get("/")
async def get_tasks(
    request: Request,
    response: Response
):
    """ Get form page and results """
    # tasks = await TaskResult.find().project(TaskView).to_list()
    tasks_main = await Task.find().project(TaskView).to_list()
    # tasks = await TaskResult.find().fetch_all()
    # tasks = await TaskResult.find().to_list()
    # tasks = [task.dict() for task in tasks]
    # print("TASKS: ", tasks_main)
    context = {"request": request, "tasks": tasks_main}
    
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

    print(f"celery with the task id started: {task_result.id}")
    
    new_task.celery_task_id = task_result.id
    await new_task.create()
    response.status_code = status.HTTP_200_OK
 
    return new_task.model_dump(exclude=["results", "scraped_urls"])
    

@router.get("/specific-task/{task_id}")
async def query_specific_task(
    request: Request,
    task_id: str,
):
    '''specifics tasks'''
    tasks = await TaskResult.find(
        {"taskId": PydanticObjectId(task_id)}
    ).to_list()
    print("this is the task", tasks)
    context = {
        "request": request,
        "data": tasks,
        "task_id": task_id
    }
    return jin_template.TemplateResponse("task.html", context)


@router.get("/download-csv/{task_id}")
async def download_csv(
    response: Response,
    task_id: str
):
    """ Download data as CSV """
    
    # Fetch data from MongoDB
    tasks_query = await TaskResult.find(
        {"taskId": PydanticObjectId(task_id)}
    ).to_list()
    tasks = [task.dict() for task in tasks_query]

    # Convert data to DataFrame
    df = pd.DataFrame(tasks)

    # Convert DataFrame to CSV
    csv_data = df.to_csv(index=False).encode("utf-8")

    # Generate a random UUID for the CSV file
    filename = f"{task_id}_{uuid.uuid4()}_tasks.csv"

    # Set response headers for download
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.headers["Content-Type"] = "text/csv"
    
    # Return a StreamingResponse with CSV data
    return StreamingResponse(iter([csv_data]), media_type="text/csv")