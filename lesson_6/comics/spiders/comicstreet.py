# -*- coding: utf-8 -*-
import scrapy


class ComicstreetSpider(scrapy.Spider):
    name = 'comicstreet'
    allowed_domains = ['comicstreet.ru']
    start_urls = ['http://comicstreet.ru/']

    def parse(self, response):
        pass
