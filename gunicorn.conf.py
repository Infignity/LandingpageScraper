# Gunicorn configuration file

import multiprocessing
from src import app_config
import os

max_requests = 1000
max_requests_jitter = 50

log_file = os.path.join(app_config.BASE_DIR, "gunicorn.log")

bind = "0.0.0.0:8080"

worker_class = "uvicorn.workers.UvicornWorker"
workers = (multiprocessing.cpu_count() * 2) + 1
