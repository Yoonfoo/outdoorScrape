import scrapy


class OspreyspiderSpider(scrapy.Spider):
    name = "ospreySpider"
    allowed_domains = ["www.opsrey.com"]
    start_urls = ["https://www.opsrey.com"]

    def parse(self, response):
        pass
