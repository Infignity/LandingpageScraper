from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from src.database import init_db
from src.router import router as ScrapeRouter
from src.models import Task, TaskResult

app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
)


app.include_router(ScrapeRouter)

MODELS = [Task, TaskResult]

@app.on_event("startup")
async def start_db():
    """Initializes the database"""
    
    await init_db(models=MODELS)
    


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "message":"Request Body Validation Error",
            "description":"There is atleast one validation error in your request body",
            "detail": jsonable_encoder(exc.errors(), exclude={"url", "type"})
        }
    )

@app.exception_handler(status.HTTP_404_NOT_FOUND)
async def not_found(request: Request, exc) -> JSONResponse:
    return JSONResponse(
        status_code = exc.status_code,
        content = {
            "message":"Not found",
            "description":"Sorry the requested resource was not found :("
        }
    )