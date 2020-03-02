# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
from scrapy.loader import ItemLoader
import re


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']

    def __init__(self, mark):
        self.start_urls = [f'https://hh.ru/search/vacancy?area=1&clusters=true&enable_snippets=true&order_by=publication_time&text={mark}&salary=']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class='bloko-button HH-Pager-Controls-Next HH-Pager-Control']/@href").extract_first()
        vacansy = response.xpath(
            "//div[@class='resume-search-item__name']//a/@href"
        ).extract()
        for link in vacansy:
            yield response.follow(link, callback=self.vacansy_parse)
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacansy_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=JobparserItem(), response=response)
        loader.add_value('_id', response.url)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('salary', "//p[@class='vacancy-salary']/text()")
        loader.add_value('link', response.url)
        loader.add_value('from_url', self.allowed_domains[0])
        yield loader.load_item()

        #name = response.xpath('//h1/text()').extract_first()
        #salary = response.xpath("//p[@class='vacancy-salary']/text()").extract()
        #link = response.url
        #yield JobparserItem(_id=link, name=name, salary=salary, link=link, from_url=self.allowed_domains[0])
