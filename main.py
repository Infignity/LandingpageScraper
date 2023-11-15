'''import libs'''
from fastapi import FastAPI
from dotenv import load_dotenv
from api.models.db import Base, engine
from api.routers.views import router as ScrapeRouter
app = FastAPI()
load_dotenv()

origins = ["*"]


Base.metadata.create_all(bind=engine)
app.include_router(ScrapeRouter)
