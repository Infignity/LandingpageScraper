# scrapify_csv

```
# run app
uvicorn src.app:app –reload
```

# run celery
```
python3 -m celery -A src.agent.celery_app worker --loglevel=info -E

```