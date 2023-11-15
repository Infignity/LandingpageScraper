"""crawler libs import"""
from agent import celery_app
from billiard import Process
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class CrawlerTrigger:
    """crawler trigger"""
    def __init__(self):
        self.crawler_process = CrawlerProcess(get_project_settings())

    def crawl(self, **kwargs):
        """crawl"""
        spider_name = "webcrawler"
        self.crawler_process.crawl(
            spider_name, url=kwargs["urls"], tags=kwargs["uuid"],
        )
        self.crawler_process.start()
        self.crawler_process.stop()
        return {
            "status": "success",
            # "data": extracted_data
        }

    def crawl_trigs(self, urls: [str], uuid: str):
        """crawl func"""
        bill_process = Process(
            target=self.crawl,
            kwargs={'urls': urls, 'uuid': uuid}
        )
        bill_process.start()
        bill_process.join()


crawler = CrawlerTrigger()


@celery_app.task(name="run_crawler")
def crawler_task(
    uuid: str,
    urls: [str]
):
    '''crawler task caller'''
    crawler.crawl_trigs(urls, uuid)
    return True
