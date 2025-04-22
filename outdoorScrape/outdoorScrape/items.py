import scrapy
from itemloaders.processors import TakeFirst, MapCompose

def remove_symbols(price):
    if price:
        return int(price.replace("NT$", "").replace(",", "").strip())
    return price

class ArcteryxProducts(scrapy.Item):
    
    name = scrapy.Field(output_processor=TakeFirst())
    catalog_number = scrapy.Field(output_processor=TakeFirst())
    old_price = scrapy.Field(
        input_processor=MapCompose(remove_symbols),
        output_processor=TakeFirst()
    )
    special_price = scrapy.Field(
        input_processor=MapCompose(remove_symbols),
        output_processor=TakeFirst()
    )
    product_url = scrapy.Field(output_processor=TakeFirst())

class MysteryProducts(scrapy.Item):
    
    product_category = scrapy.Field(output_processor=TakeFirst())
    product_name = scrapy.Field(output_processor=TakeFirst())
    product_url = scrapy.Field(output_processor=TakeFirst())
    product_price = scrapy.Field(
        input_processor=MapCompose(remove_symbols),
        output_processor=TakeFirst()
    )
    product_image = scrapy.Field(output_processor=TakeFirst())
    product_volume = scrapy.Field(output_processor=TakeFirst())
    product_weight = scrapy.Field(output_processor=TakeFirst())
    product_height = scrapy.Field(output_processor=TakeFirst())
    product_width = scrapy.Field(output_processor=TakeFirst())
    product_depth = scrapy.Field(output_processor=TakeFirst())