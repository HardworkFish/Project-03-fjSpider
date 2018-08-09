# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GFsundeES_fangItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()  # 标题
    price_total = scrapy.Field()  # 总价
    house_type = scrapy.Field()  # 户型
    house_area = scrapy.Field()  # 建筑面积
    price_averages = scrapy.Field()  # 单价
    house_towards = scrapy.Field()  # 朝向
    total_floor = scrapy.Field()  # 楼层数
    house_floor = scrapy.Field()  # 楼层
    decoration = scrapy.Field()  # 装修
    neighborhood = scrapy.Field()  # 小区
    location = scrapy.Field()  # 位置
    house_age = scrapy.Field()  # 建筑年代
    structure = scrapy.Field()  # 建筑结构
    property_right = scrapy.Field()  # 产权性质
    residential_category = scrapy.Field()  # 住宅类别
    construction_category = scrapy.Field()  # 建筑类别
    listed_time = scrapy.Field()  # 挂牌时间
    description = scrapy.Field()  # 房源描述
    contact = scrapy.Field()  # 联系人
    belong = scrapy.Field()  # 联系人所属
    phone_number = scrapy.Field()  # 联系方式


class GFsundeXQ_fangItem(scrapy.Item):
    url = scrapy.Field()
    neighborhood = scrapy.Field()  # 小区名称
    open_date = scrapy.Field()  # 开盘时间
    subhouse_date = scrapy.Field()  # 交房时间
    price_averages = scrapy.Field()  # 本月均价
    adress = scrapy.Field()  # 小区地址
    location = scrapy.Field()  # 所在区域
    neigh_type = scrapy.Field()  # 物业类型
    building_type = scrapy.Field()  # 建筑类型
    neigh_area = scrapy.Field()  # 占地面积
    building_area = scrapy.Field()  # 建筑面积
    volumetric_rate = scrapy.Field()  # 容积率
    total_floor = scrapy.Field()
    house_age = scrapy.Field()


class GDSZES_fangItem(scrapy.Item):
    url = scrapy.Field()
    price_avg = scrapy.Field()
    location = scrapy.Field()
