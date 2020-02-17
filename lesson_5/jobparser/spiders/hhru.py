# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
import re


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    search_s = input('Введите название вакансии: ')
    search = re.sub(r'\s', '+', search_s)
    start_urls = [f'https://hh.ru/search/vacancy?area=1&clusters=true&enable_snippets=true&order_by=publication_time&text={search}&salary=']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class='bloko-button HH-Pager-Controls-Next HH-Pager-Control']/@href").extract_first()
        vacansy = response.xpath(
            "//div[@class='resume-search-item__name']//a/@href"
        ).extract()
        for link in vacansy:
            yield response.follow(link, callback=self.vacansy_parse)
        yield response.follow(next_page, callback=self.parse)

    def vacansy_parse(self, response: HtmlResponse):
        name = response.xpath('//h1/text()').extract_first()
        salary = response.xpath("//p[@class='vacancy-salary']/text()").extract()
        link = response.url
        yield JobparserItem(_id=link, name=name, salary=salary, link=link, from_url=self.allowed_domains[0])
