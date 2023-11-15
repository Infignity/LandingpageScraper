"""item module definitions"""
import scrapy


class WebcrawlerItem(scrapy.Item):
    """package fields"""
    tag = scrapy.Field()
    url = scrapy.Field()
    text = scrapy.Field()
