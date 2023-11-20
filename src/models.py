from beanie.odm.documents import Document
from beanie import PydanticObjectId
from typing import List, Dict, Literal, Set
from pydantic import Field
from src.app_config import simple_pydantic_model_config
from datetime import datetime

class TaskResult(Document):
    class Settings:
        name = "task_results"
        use_state_management = True
    
    model_config = simple_pydantic_model_config
    
    id: PydanticObjectId = Field(
        description="Task result Id",
        default_factory=lambda: PydanticObjectId(),
        alias="_id"
    )
    
    task_id: PydanticObjectId
    landing_page_text: str
    url: str
    

class Task(Document):
    class Settings:
        name = "tasks"
        use_state_management = True
        # projection = {"results":0}
        
    model_config = simple_pydantic_model_config
    
    id: PydanticObjectId = Field(
        description="Task Id",
        default_factory=lambda: PydanticObjectId(),
        alias="_id"
    )
    
    celery_task_id: str = Field(default="")
    registered_at: datetime = Field(default_factory=datetime.now)
    state: Literal["completed", "running", "notstarted"] = Field(default="notstarted")
    results: List[TaskResult] = Field(default=[])
    scraped_urls: List = Field(default = [])
    

    
    