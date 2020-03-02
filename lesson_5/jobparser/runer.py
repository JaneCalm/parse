from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jobparser import settings
from jobparser.spiders.hhru import HhruSpider
from jobparser.spiders.sjru import SjruSpider
import re
import transliterate

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    search_s = input('Введите название вакансии: ')
    search = re.sub(r'\s', '+', search_s)
    search_two = transliterate.translit(search_s, reversed=True)
    search_two = re.sub(r'\s', '-', search_two)
    process.crawl(HhruSpider,mark=search)
    process.crawl(SjruSpider,mark=search_two)
    process.start()