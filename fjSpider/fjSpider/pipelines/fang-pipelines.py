# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from fjSpider.store import *


class GFsundeESPipeline(object):
    def process_item(self, item, spider):
        spec = {'title': item['title'],
                'price_total': item['price_total']}
        GFsundeES.update(spec, {'$set': item}, upsert=True)
        return None


class GFsundeXQPipeline(object):
    def process_item(self, item, spider):
        spec = {'neighborhood': item['neighborhood']}
        GFsundeXQ.update(spec, {'$set': item}, upsert=True)
        return item


class GDSZESPipeline(object):
    def process_item(self, item, spider):
        spec = {'url': item['url']}
        GDSZES.update(spec, {'$set': item}, upsert=True)
