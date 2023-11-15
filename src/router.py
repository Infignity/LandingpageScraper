'''lib import'''
import uuid
from io import BytesIO
import pandas as pd
from fastapi import (
    APIRouter, 
    Request, 
    status, 
    Depends, 
    UploadFile, File, HTTPException)
import os  
from fastapi.responses import JSONResponse
from starlette.templating import Jinja2Templates
from sqlalchemy.orm import Session
from src.request_schemas import TranslationRequest
from src.models import CompanyModel
from src.database import connect_db
from src.agent.tasks import crawler_task
from src.app_config import BASE_DIR
from src import read_csv_file

router = APIRouter()
jin_template = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


@router.get("/")
def index(
    request: Request,
    db: Session = Depends(connect_db)
):
    """ Get form page and results """
    
    companies_data = db.query(CompanyModel).all()
    result_list = []
    # Loop through the data and create dictionaries
    for item in companies_data:
        result_dict = {
            "id": item.id,
            "url": item.url,
            "tag": item.tag,
            "text": item.text,
        }
        result_list.append(result_dict)
    context = {"request": request, "data": result_list}
    return jin_template.TemplateResponse("index.html", context)


@router.get("/ping")
async def root():
    """a test route"""
    return {"message": "ping pong"}


@router.post('/scrape')
def register_task(
    file: UploadFile = File(...)
):
    """ Register new scraping task """
    
    content = {}
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


    # a random uuid to track celery task
    random_uuid = str(uuid.uuid4())
    
    # call task multiple time to ensure success
    task_result = crawler_task.delay(
        random_uuid,
        urls,
    )

    task_id = task_result.id
    if task_result.successful():
        # Get the result of the task
        data = task_result.result
        content["data"] = data
        
        return JSONResponse(
            content=content,
            status_code=status.HTTP_200_OK
        )
    else:
        content["task_id"] = task_id
        return JSONResponse(
            content=content,
            status_code=status.HTTP_200_OK
        )


@router.get("/scrapped")
def get_scrapped(request: Request):
    """ get all scrapped data """
    content = {}
    return JSONResponse(
        content=content,
        status_code=status.HTTP_200_OK
    )

