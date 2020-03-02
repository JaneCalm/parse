# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import transliterate
from scrapy.loader.processors import MapCompose, TakeFirst
import re


def cleaner_photo(values):
    if values:
        return values
    return


def int_val(values):
    if values:
        result = []
        search = re.sub('\s','',values)
        search_int = re.findall('\d+', search)[0]
        search_val = re.findall('\D+', search)[0]
        result.append(int(search_int))
        result.append(search_val)
        return result
    return


class ComicsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    price = scrapy.Field(input_processor=MapCompose(int_val))
    char = scrapy.Field()
    char_names = scrapy.Field()

    def __setitem__(self, key, value):
        if key not in self.fields:
            self.fields[key] = scrapy.Field()
        super(ComicsItem, self).__setitem__(key, value)
    pass

