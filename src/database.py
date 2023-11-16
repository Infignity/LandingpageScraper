""" Includes code to communicate with mongodb database """

from typing import List
import motor.motor_asyncio
from beanie import init_beanie
from src.app_config import (
    DB_NAME,
    MONGODB_CONN_STRING,
)


async def init_db(models: List):
    """
    Initializes the database connection using async motor driver
    :param models: A list of models to add
    """
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_CONN_STRING)
    await init_beanie(
        database=client.get_default_database(DB_NAME), document_models=models
    )