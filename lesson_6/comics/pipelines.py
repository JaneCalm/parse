# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import transliterate
import re

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
import os
from urllib.parse import urlparse


class DataBasePipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.comics_photo

    def process_item(self, item, spider):
        _id = item['_id']
        char = item['char']
        char_names = item['char_names']
        for i in range(len(char_names)):
            name_char = re.sub('\W','',char_names[i])
            name_char = re.sub("ь", '', name_char)
            if name_char not in 'ISBN':
                name_char = transliterate.translit(name_char, reversed=True)
            item[str(name_char)] = char[i]
        del item['char']
        del item['char_names']
        collection = self.mongo_base[spider.name]
        exists = collection.count_documents({'_id': {'$eq': _id}})
        if exists is 0:
            collection.insert_one(item)
        else:
            collection.update_one({'_id': _id}, {'$set': item})
        return item


class ComicsPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img, meta={'image_from': item['name']})
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None):
        image_from = re.sub('/', '_', request.meta['image_from'])
        image_from = re.sub('\s', '', image_from)
        name = re.split('/', request.url)[-1]
        name = re.sub('\s', '', name)
        name = name[-10:]
        return f'{image_from}/{name}'

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item
