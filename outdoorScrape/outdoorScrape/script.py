import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.arcteryxSpider import ArcteryxSpider
from spiders.mysterySpider import MysterySpider


process = CrawlerProcess(get_project_settings())

process.crawl(ArcteryxSpider)
process.crawl(MysterySpider)
process.start()
