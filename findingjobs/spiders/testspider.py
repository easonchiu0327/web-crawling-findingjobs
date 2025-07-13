# findingjobs/spiders/testspider.py
import scrapy

class TestSpider(scrapy.Spider):
    name = "testspider"
    start_urls = ['http://httpbin.org/json']

    def parse(self, response):
        yield {
            'hello': 'world',
            'url': response.url,
        }