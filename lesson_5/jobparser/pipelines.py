# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import re


def hh_clean(item):
    salary_min = 0
    salary_max = 0
    salary_val = None
    salary = ''.join(item['salary'])
    hm = re.findall(r'^от_*', salary)
    hm2 = re.findall(r'^до_*', salary)
    if hm:
        salary = re.sub(r'на руки', '', salary)
        salary = re.sub(r'до вычета налогов', '', salary)
        salary = re.sub(r'\s', '', salary)
        hm3 = re.search(r'до', salary)
        if hm3:
            hm_num = re.sub(r'до', '-', salary)
            hm_num = re.split(r'-', hm_num)
            hm_num1 = hm_num[0]
            hm_num2 = hm_num[1]
            salary_min = int(re.sub(r'от', '', hm_num1))
            hm_val = re.search(r'[\D]+', hm_num2)
            salary_max = int(re.sub(r'[\D]+', '', hm_num2))
            salary_val = hm_val[0]
        else:
            hm_num = re.sub(r'от', '', salary)
            salary_val = re.search(r'[\D]+', hm_num)
            salary_val = salary_val[0]
            salary_min = int(re.sub(r'[\D]+', '', hm_num))

    if hm2:
        salary = re.sub(r'на руки', '', salary)
        salary = re.sub(r'до вычета налогов', '', salary)
        salary = re.sub(r'\s', '', salary)
        hm_num = re.sub(r'до', '', salary)
        salary_val = re.search(r'[\D]+', hm_num)
        salary_val = salary_val[0]
        salary_max = int(re.sub(r'[\D]+', '', hm_num))

    item['salary_min'] = salary_min
    item['salary_max'] = salary_max
    item['salary_val'] = salary_val
    del item['salary']

    return item


def sj_clean(item):
    salary_min = 0
    salary_max = 0
    salary_val = None
    salary = ''.join(item['salary'])
    hm = re.findall(r'^от_*', salary)
    hm2 = re.findall(r'^до_*', salary)
    hm3 = re.findall(r'—', salary)
    hm4 = re.search(r'[\d]+', salary)
    if hm:
        salary = re.sub(r'\s', '', salary)
        hm_num = re.sub(r'от', '', salary)
        salary_val = re.search(r'[\D]+', hm_num)
        salary_val = salary_val[0]
        salary_min = int(re.sub(r'[\D]+', '', hm_num))
    elif hm2:
        salary = re.sub(r'\s', '', salary)
        hm_num = re.sub(r'до', '', salary)
        salary_val = re.search(r'[\D]+', hm_num)
        salary_val = salary_val[0]
        salary_max = int(re.sub(r'[\D]+', '', hm_num))
    elif hm3:
        salary = re.sub(r'\s', '', salary)
        hm_num = re.split(r'—', salary)
        salary_min = int(hm_num[0])
        hm_num2 = hm_num[1]
        hm_val = re.search(r'[\D]+', hm_num2)
        salary_max = int(re.sub(r'[\D]+', '', hm_num2))
        salary_val = hm_val[0]
    elif hm4:
        hm_num = re.sub(r'\s', '', salary)
        salary_val = re.search(r'[\D]+', hm_num)
        salary_val = salary_val[0]
        salary_min = int(re.sub(r'[\D]+', '', hm_num))
        salary_max = salary_min

    item['salary_min'] = salary_min
    item['salary_max'] = salary_max
    item['salary_val'] = salary_val
    del item['salary']
    return item


class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacansy_scrapy

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            item = hh_clean(item)

        if spider.name == 'sjru':
            item = sj_clean(item)

        link = item['link']
        collection = self.mongobase[spider.name]
        exists = collection.count_documents({'_id': {'$eq': link}})
        if exists is 0:
            collection.insert_one(item)
        else:
            collection.update_one({'_id': link}, {'$set': item})

        return item
