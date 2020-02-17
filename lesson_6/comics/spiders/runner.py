from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from comics.spiders.comicstreet import ComicstreetSpider
from comics import settings
import re

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    search = input("Введите слово для поиска: ")
    search = re.sub('\s','+',search)
    process.crawl(ComicstreetSpider, mark=search)
    process.start()