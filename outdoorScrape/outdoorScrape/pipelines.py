# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import mysql.connector
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class ArcteryxPipeline:
    
    table_name = "arcteryx"
    
    def open_spider(self, spider):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="outdoorgeardb",
            charset="utf8mb4",
            use_unicode=True,
        )
        self.cursor = self.conn.cursor()
        
    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
        
    def process_item(self, item, spider):
        
        sql = """
        INSERT INTO arcteryx (product_name, product_catalog_number, product_old_price, product_special_price, product_url)
        VALUES (%s, %s, %s, %s, %s)
        """
        value = (
            item['name'],
            item['catalog_number'],
            item['old_price'],
            item['special_price'],
            item['product_url']
        )
        
        try:
            self.cursor.execute(sql, value)
            self.conn.commit()
        except Exception as e:
            raise DropItem(f"Error inserting item into database: {e}")
        
        return item

class MysteryPipeline:
    
    table_name = "mystery"
    
    def open_spider(self, spider):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="outdoorgeardb",
            charset="utf8mb4",
            use_unicode=True,
        )
        self.cursor = self.conn.cursor()
        
    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
        
    def process_item(self, item, spider):
        
        sql = """
        INSERT INTO mystery (product_category, product_name, product_url, product_price, product_image, product_volume, product_weight, product_height, product_width, product_depth)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
    
        value = (
            item.get('product_category'),
            item.get('product_name'),
            item.get('product_url'),
            item.get('product_price'),
            item.get('product_image'),
            item.get('product_volume') or None,
            item.get('product_weight') or None,
            item.get('product_height') or None,
            item.get('product_width') or None,
            item.get('product_depth') or None
        )
        
        try:
            self.cursor.execute(sql, value)
            self.conn.commit()
        except Exception as e:
            raise DropItem(f"Error inserting item into database: {e}")
        
        return item