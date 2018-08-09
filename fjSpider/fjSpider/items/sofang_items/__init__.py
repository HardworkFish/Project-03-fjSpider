# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class sofangItem(scrapy.Item):
    house_name = scrapy.Field()
    house_time = scrapy.Field()
    house_tag = scrapy.Field()
    price_total = scrapy.Field()
    price_averages = scrapy.Field()
    house_pattern = scrapy.Field()
    house_area = scrapy.Field()
    house_towards = scrapy.Field()
    house_floor = scrapy.Field()
    house_type = scrapy.Field()
    house_age = scrapy.Field()
    property_name = scrapy.Field()
    location = scrapy.Field()
    position_x = scrapy.Field()
    position_y = scrapy.Field()
    description = scrapy.Field()
