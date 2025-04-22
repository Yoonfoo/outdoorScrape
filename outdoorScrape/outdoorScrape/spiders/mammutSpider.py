import scrapy


class MammutspiderSpider(scrapy.Spider):
    name = "mammutSpider"
    allowed_domains = ["www.mammut.tw"]
    start_urls = ["https://www.mammut.tw"]

    def parse(self, response):
        pass
