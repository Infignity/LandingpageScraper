from beanie.odm.documents import Document
from beanie import PydanticObjectId
from typing import List, Dict, Literal
from pydantic import Field
from src.app_config import simple_pydantic_model_config
from datetime import datetime


class Task(Document):
    class Settings:
        name = "tasks"
        use_state_management = True
        
    model_config = simple_pydantic_model_config
    
    id: PydanticObjectId = Field(
        description="Task Id",
        default_factory=lambda: PydanticObjectId(),
        alias="_id"
    )
    
    celery_task_id: str = Field(default="")
    registered_at: datetime = Field(default_factory=datetime.now)
    state: Literal["completed", "running", "notstarted"] = Field(default="notstarted")
    results: List[Dict] = Field(default=[])
    
