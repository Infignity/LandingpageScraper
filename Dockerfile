FROM python:3.10

COPY . /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8057

CMD [ "gunicorn" , "src.app:app"]
