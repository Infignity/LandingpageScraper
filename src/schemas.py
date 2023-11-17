from pydantic import BaseModel, Field
from beanie import PydanticObjectId
from src.app_config import simple_pydantic_model_config
from typing import Literal, List
from datetime import datetime

class TaskView(BaseModel):
    model_config = simple_pydantic_model_config
    
    id: PydanticObjectId = Field(alias="_id")
    celery_task_id: str
    registered_at: datetime
    state: Literal["completed", "running", "notstarted"]