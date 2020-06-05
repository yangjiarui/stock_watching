# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

db=pymongo.MongoClient('localhost',27017)['雪球财经']

class XqproPipeline(object):
    def process_item(self, item, spider):
        db['0603'].insert_one(dict(item))
        return item
