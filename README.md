# Landingpage Scraper

Robust web crawler for scraping the landing pages of websites. Aim is to get input content for email generation using gpt models & llms. For instance, we pass in a csv of companies, this crawler goes through all.. the company websites and generates an output csv with 3 columns, company name , company url and landing page text. This text is then given to a gpt model with a prompt to generate customized email for that company.

This project uses httpx behind then scenes to send asynchronous requests which is more faster than sending individual requests. It also uses [beanie](https://beanie-odm.dev) which is an async odm for mongodb.

For more reference . There are 2 models
- Task - For storing all tasks
- TaskResult - For storing the task results and using the task_id as some sort of primary key to connect the Task collection

## Limitations
- Cannot extract landing page text for bot protected websites
- Some websites need cookies and javascript to be enabled before accessing it
- Some websites are country restricted.

## Proposed solutions
- Consider using automated webdrivers :: Solves the problem of javascript and cookies being enabled.
- Run every scraping task in a docker container because there is a limit to how many browser instances you can have on a single machine.

## Running project
This project consists of 2 main parts, the api and the celery worker for web scraping. Note that you need to have redis installed and running on port 6379

```bash
# Run redis using docker
docker run --name redis -p 6379:6379 --restart always redis:latest

# Clone project
gh repo clone infignity/LandingpageScraper
cd LandingpageScraper

# Create a virtual environment and install requirements
python3 -m pip install virtualenv
python3 -m virtualenv landingpage-scraper
source landingpage-scraper/bin/activate
python3 -m pip install -r requirements.txt

# Start api - add --reload for debug mode
uvicorn src.app:app --host 0.0.0.0 --port 8000

# Start celery worker 
celery -A src.agent.celery_app worker --loglevel=info -E
```

For vscode debugging you can add this configuration in the .vscode/launch.json file.

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Api",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "src.app:app",
                "--reload"
            ],
            "jinja": true,
            "justMyCode": true
        },
        {
            "name": "Celery Worker",
            "type": "python",
            "request": "launch",
            "module": "celery",
            "args": [
                "-A",
                "src.agent.celery_app",
                "worker",
                "--loglevel=info",
                "-E"
            ],
            "jinja": true,
            "justMyCode": true
        }
    ]
}
```