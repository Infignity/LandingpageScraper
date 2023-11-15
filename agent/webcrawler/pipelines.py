""" scrappy item libs"""
import os
import psycopg2
from itemadapter import ItemAdapter
from dotenv import load_dotenv
load_dotenv()


class WebcrawlerPipeline:
    """database serving class"""
    def __init__(self):
        # Connection Details
        hostname = 'localhost'
        username = os.getenv("DB_USER")
        password = os.getenv("DB_PASS")
        database = os.getenv("DB_NAME")
        # Create/Connect to database
        self.connection = psycopg2.connect(
            host=hostname,
            user=username,
            password=password,
            dbname=database
        )
        # Create cursor, used to execute commands
        self.cur = self.connection.cursor()
        # Create campaign table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS web_scrapper(
            id serial PRIMARY KEY,
            tag text,
            url text,
            text text
        )
        """)

    def process_item(self, item, spider):
        """process item func"""
        print("inserted into DB")
        self.cur.execute(
            """ insert into web_scrapper (tag, url, text ) values (%s,%s,%s)""",
            (item["tag"], item["url"], item["text"])
        )
        # Execute insert of data into database
        self.connection.commit()
        return item
    
    def close_db(self, spider):
        """closing database connection"""
        self.cur.close()
        self.connection.close()
