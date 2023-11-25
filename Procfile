web: uvicorn src.app:app --host 0.0.0.0 --port 80
celery: celery -A src.agent.celery_app worker --loglevel=info -E