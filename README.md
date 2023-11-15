# scrapify_csv

```
# run app
uvicorn main:app –reload
```

# run celery
```
python3 -m celery -A agent worker --loglevel=info

python3 -m celery -A agent  worker --loglevel=info

```

# connect o sql using terminal
```
psql postgres
```

# creating database
```
create database campaign;
create user myuser with encrypted password 'mypass';
grant all privileges on database mydb to myuser;
grant usage on schema public to campaign_user;
grant usage on all sequences in schema public to <myuser>
```
web_camp;