# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    salary = scrapy.Field()
    link = scrapy.Field(output_processor=TakeFirst())
    from_url = scrapy.Field(output_processor=TakeFirst())

    def __setitem__(self, key, value):
        if key not in self.fields:
            self.fields[key] = scrapy.Field()
        super(JobparserItem, self).__setitem__(key, value)
    pass
