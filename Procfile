web: uvicorn src.app:app --workers 4
celery: celery -A src.agent.celery_app worker --loglevel=info