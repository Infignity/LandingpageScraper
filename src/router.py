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
    
from fastapi.responses import JSONResponse
from starlette.templating import Jinja2Templates
from sqlalchemy.orm import Session
from src.request_schemas import TranslationRequest
from src.models import CompanyModel
from src.database import connect_db
from src.agent.tasks import crawler_task


router = APIRouter()
jin_template = Jinja2Templates(directory="api/templates")


# helpers function
def read_csv_file(file_name, column_index='organization_website'):
    """Read the CSV file and extract a specific column."""
    df = pd.read_csv(file_name)
    # Extract the specified column
    urls = df[column_index].tolist()
    return urls

# @router.get("/", name="home")
# def query_home(
#     request: Request,
# ):
#     """entry page"""
#     context = {"request": request, "data": "test"}
#     return jin_template.TemplateResponse("index.html", context)

@router.get("/")
def query_home(
    request: Request,
    db: Session = Depends(connect_db)
):
    '''get all AI queries'''
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


@router.post('/scrape',)
def scrape_url(
    file: UploadFile = File(...)
):
    '''web scrapper'''
    content = {}

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

    formatted_urls = set()
    for url in urls:
        # if 'http' not in url:
        #     url = 'https://' + url
        formatted_urls.add(url)

    start_urls = list(formatted_urls)
    # a random uuid to track celery task
    random_uuid = str(uuid.uuid4())
    
    # call task multiple time to ensure success
    task_result = crawler_task.delay(
        random_uuid,
        start_urls,
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
    """get all scrapped data"""
    content = {}
    return JSONResponse(
        content=content,
        status_code=status.HTTP_200_OK
    )

