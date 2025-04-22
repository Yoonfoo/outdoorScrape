import scrapy
from outdoorScrape.items import ArcteryxProducts
from typing import Generator
from scrapy.http import Response
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

class ArcteryxSpider(scrapy.Spider):
    name: str = "arcteryxSpider"
    allowed_domains: list[str] = ["www.arcteryx.com.tw"]
    start_urls: list[str] = ["https://www.arcteryx.com.tw/"]
    custom_settings: dict = {
        'ITEM_PIPELINES': {
            'outdoorScrape.pipelines.ArcteryxPipeline': 300,
        },
    }


    category_link_extractor = LinkExtractor(allow=r"(men|women)/(clothing|packs|shoes|accessories)/.+")
    product_link_extractor = LinkExtractor(allow=r"x\d+(-\w+)?\.html")
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
    def parse(self, response: Response) -> Generator[Response, None, None]:
        links = self.category_link_extractor.extract_links(response)
        
        for link in links:
            yield response.follow(link.url, callback=self.extract_product_links)
    
    def extract_product_links(self, response: Response):
        links = self.product_link_extractor.extract_links(response)
        for link in links:
            yield response.follow(link.url, callback=self.parse_product_page)
    
    def parse_product_page(self, response: Response):
        
        arcteryx_product = ItemLoader(ArcteryxProducts(), response=response)
        arcteryx_product.add_xpath('name','//h1[@class="page-title"]/span/text()')
        arcteryx_product.add_xpath('catalog_number','//*[@id="maincontent"]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div[2]/div/div/text()')
        arcteryx_product.add_xpath('old_price','/html/body/div[2]/main/div[2]/div/div[1]/div[1]/div[2]/form/div[3]/div[2]/div/span[1]/span/span[2]/span/text()')
        arcteryx_product.add_xpath('special_price','/html/body/div[2]/main/div[2]/div/div[1]/div[1]/div[2]/form/div[3]/div[2]/div/span[2]/span/span[2]/span/text()')
        arcteryx_product.add_value('product_url', response.url)
                
        yield arcteryx_product.load_item()
    