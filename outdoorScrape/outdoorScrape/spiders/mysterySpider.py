import scrapy
import logging
from itemloaders import ItemLoader
from outdoorScrape.items import MysteryProducts
from typing import Generator
from scrapy.http import Response
from scrapy.linkextractors import LinkExtractor

class MysterySpider(scrapy.Spider):
    name : str = "mysterySpider"
    allowed_domains : list[str] = ["www.mysteryranch.tw"]
    start_urls : list[str] = ["https://www.mysteryranch.tw"]
    custom_settings : dict = {
        'ITEM_PIPELINES': {
            'outdoorScrape.pipelines.MysteryPipeline': 300,
        },
    }

    category_link_extractor = LinkExtractor(allow=r"product/product_list.html\?cata=[^#]+$")

    def parse(self, response : Response) -> Generator[Response, None, None]:
        links = self.category_link_extractor.extract_links(response)
        for link in links:
            yield response.follow(link.url, callback=self.extract_product_links)
            
    def extract_product_links(self, response : Response) -> Generator[Response, None, None]:
        category_group = response.xpath('//div[@class="productGroup"]')
        
        for category in category_group:
            product_category = category.xpath('h2/text()').get()
            product_lists = category.xpath('ul/li')
            if product_lists:
                for product in product_lists:
                    mystery_product = ItemLoader(MysteryProducts())
                    product_name = product.xpath('figcaption/a/text()').get()
                    product_link = product.xpath('.//a[@class="btnMore"]/@href').get()
                    product_price = product.xpath('span[@class="price"]/text()').get()
                    
                    mystery_product.add_value('product_category', product_category)
                    mystery_product.add_value('product_name', product_name.strip())
                    mystery_product.add_value('product_url', product_link)
                    mystery_product.add_value('product_price', product_price)
                    
                    yield response.follow(product_link, callback=self.extract_product_details, meta={'items': mystery_product})
                    
                    
    def extract_product_details(self, response : Response) -> Generator[Response, None, None]:
        
            mystery_product = response.meta['items']
            product_img = response.xpath('//div[@class="insideContent"]//img/@src').get()
            product_spec = response.xpath('//div[@class="specification"]/p/text()').getall()
            
            for spec in product_spec:
                if '容量' in spec:
                    product_volume = float(spec.replace('容量：', '').replace('L','').strip())
                elif '重量' in spec:
                    if 'kg' in spec:
                        product_weight = float(spec.replace('重量：', '').replace('kg','').strip()) 
                    elif 'g' in spec:
                        product_weight = float(spec.replace('重量：', '').replace('g','').strip()) / 1000
                elif '尺寸' in spec:
                    product_size = spec.replace('尺寸：', '').replace('cm','').strip().split('x')
                    if len(product_size) == 2:
                        product_height = float(product_size[0])
                        product_width = float(product_size[1])
                    elif len(product_size) == 3:
                        product_height = float(product_size[0])
                        product_width = float(product_size[1])
                        product_depth = float(product_size[2])

            mystery_product.add_value('product_image', product_img)
            fields = ['product_volume', 'product_weight', 'product_height', 'product_width', 'product_depth']

            for field in fields:
                value = locals().get(field)
                if value is not None:
                    try:
                        mystery_product.add_value(field, value)
                    except Exception:
                        logging.warning(f"{field.replace('_', ' ').title()} not found for {mystery_product.get_output_value('product_name')}")
                
            yield mystery_product.load_item()

