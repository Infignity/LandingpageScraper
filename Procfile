web: uvicorn src.app:app
celery: celery -A src.agent.celery_app worker --loglevel=info