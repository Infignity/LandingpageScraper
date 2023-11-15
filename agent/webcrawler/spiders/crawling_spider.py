"""crawler spider"""
import scrapy
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import pandas as pd
from webcrawler.items import WebcrawlerItem


class CrawlingWeb(scrapy.Spider):
    """web spiders for company website scrapping"""
    name = "webcrawler"

    def __init__(self, url=None, tags=None, *args, **kwargs):
        """constructor class"""
        super(CrawlingWeb, self).__init__(*args, **kwargs)
        self.start_urls = url
        self.tags = tags
        self.data = []

    def start_requests(self):
        yield scrapy.Request(
            self.start_urls[0],
            meta={'playwright': True}
        )
  
    def parse(self, response, tag="home", flag=True):
        """parse func"""
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
        except AttributeError:
            print('Response not text:', response.status, response.headers)
            soup = BeautifulSoup('')
        link_extractor = LinkExtractor(allow="about")
        extracted_text = ' '.join(str(
            soup.get_text().replace("\n", " ")).split())
        dt = {
            "url": response.url,
            "tag": tag,
            "text": extracted_text
        }
      
        item = WebcrawlerItem()
        item["tag"] = tag
        item["url"] = response.url
        item["text"] = extracted_text
        yield item

        self.data.append(dt)
        for link in link_extractor.extract_links(response):
            yield response.follow(
                url=link.url,
                cb_kwargs=dict(tag="about", flag=False)
            )
