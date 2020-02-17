# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from comics.items import ComicsItem
from scrapy.loader import ItemLoader


class ComicstreetSpider(scrapy.Spider):
    name = 'comicstreet'
    allowed_domains = ['comicstreet.ru']
    start_urls = ['https://www.comicstreet.ru/collection/artbuki-entsiklopedii']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath(
            "//a[@class='pagination-link pagination-next']/@href").extract_first()
        ads_links = response.xpath("//div[@id='insales-section-collection']//form/a/@href").extract()
        for link in ads_links:
            yield response.follow(link, callback=self.parse_ads)
        yield response.follow(next_page, callback=self.parse)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=ComicsItem(), response=response)
        loader.add_value('_id', response.url)
        loader.add_xpath('name',"//h1[@class='product-title']/text()")
        loader.add_xpath('price',"//span[contains(@class, 'product-price')]/text()")
        loader.add_xpath('photos',"//a[contains(@class,'js-product-gallery-thumb product-gallery-thumb')]/@href")
        loader.add_xpath('char', "//div[@class='product-properties']//dd/text()|//div[@class='product-properties']//dd//span/text()")
        loader.add_xpath('char_names', "//div[@class='product-properties']//dt/span/text()")


        yield loader.load_item()
