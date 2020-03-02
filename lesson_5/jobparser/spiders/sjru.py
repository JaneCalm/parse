# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
from scrapy.loader import ItemLoader


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']

    def __init__(self, mark):
        self.start_urls = [f'https://superjob.ru/vakansii/{mark}.html?geo%5Bt%5D%5B0%5D=4']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class='icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe']/@href").extract_first()
        vacansy = response.xpath(
            "//a[contains(@class, '_1QIBo')]/@href"
        ).extract()
        for link in vacansy:
            yield response.follow(link, callback=self.vacansy_parse)
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacansy_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=JobparserItem(), response=response)
        loader.add_value('_id', response.url)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('salary', "//span[@class='_3mfro _2Wp8I ZON4b PlM3e _2JVkc']//text()")
        loader.add_value('link', response.url)
        loader.add_value('from_url', self.allowed_domains[0])
        yield loader.load_item()

        #name = response.xpath('//h1/text()').extract_first()
        #salary = response.xpath("//span[@class='_3mfro _2Wp8I ZON4b PlM3e _2JVkc']//text()").extract()
        #link = response.url
        #yield JobparserItem(_id=link, name=name, salary=salary, link=link, from_url=self.allowed_domains[0])