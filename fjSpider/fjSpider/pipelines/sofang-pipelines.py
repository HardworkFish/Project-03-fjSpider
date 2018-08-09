# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from fjSpider.store import *


class sofangPipeline(object):
    def process_item(self, item, spider):
       # spec = {'house_name': item['house_name'],
          #      'house_time': item['house_time']}
      #  FJDB.sofang.update(spec, {'$set': item}, upsert=True)
        return item
