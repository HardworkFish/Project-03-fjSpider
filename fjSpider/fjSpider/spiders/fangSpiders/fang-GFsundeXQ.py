# -*-coding:utf-8-*-  
from re import search
from urllib.parse import urljoin
import requests

from bs4 import BeautifulSoup
from scrapy import FormRequest, Request
from scrapy.spiders import Spider
from scrapy_splash import SplashRequest
from pyquery import PyQuery as pq 
from fjSpider.items.fang_items import *

# 顺德二手房房价信息


class GFsundeXQSpider(Spider):
    name = 'fang-GFsundeXQ'
    url = 'http://esf.fs.fang.com/housing/617__0_0_0_0_%d_0_0/'
    custom_settings = {
        'ITEM_PIPELINES': {
            'fjSpider.pipelines.fang-pipelines.GFsundeXQPipeline': 300,
        },
        # 渲染服务的url
        'SPLASH_URL': 'http://localhost:8050',

        # 下载器中间件
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'fjSpider.middlewares.userAgentMiddleware': 500,
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
        },
        'SPIDER_MIDDLEWARES': {
            'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
        },
        # 去重过滤器
        'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
        # 使用Splash的Http缓存
        'HTTPCACHE_STORAGE': 'scrapy_splash.SplashAwareFSCacheStorage',
        'DOWNLOAD_DELAY': 5,
    }

    def start_requests(self):
        for i in range(1, 2):
            # js解析用splash
            yield SplashRequest(self.url % i, callback=self.parse)

    def parse(self, response):
        #soup = BeautifulSoup(response.body, 'lxml', from_encoding='utf-8')
        #dls = soup.find_all('dl', class_='plotListwrap clearfix')
        # print(dls)    
        doc = pq(response.body.decode('utf-8'))
        for i in doc('a').filter('.plotTit').items():
            link  = 'http:'+ (i.attr('href')).split('/')[2]+'/xiangqing'
          #  print(link)
            #yield Request(link, callback=self.second_parse) 
        #for dl in dls:
         #   url = dl.find('a', class_='plotTit')
          #  print(url)
           
            #print(link)
            #url = url['href'] + 'xiangqing/'
            #item = GFsundeXQ_fangItem()
            #item['house_age'] = dl.find('ul').find_all(
             #   'li')[-1].get_text().strip()
        #link = 'http://fenghuangwanbgy0757.fang.com/xiangqing'
        
            yield SplashRequest(link, callback=self.second_parse)

    def second_parse(self, response):
        print(response.url)
        soup = BeautifulSoup(response.body, 'lxml', from_encoding='utf-8')
        #print(soup)
        item = GFsundeXQ_fangItem()
        #print(item)
        dds = soup.find('div', class_='inforwrap clearfix').find_all('dd')
        rate_box = soup.find('div', class_='box detaiLtop mt20 clearfix')
        item['url'] = response.url[:-10]
        item['neighborhood'] = soup.find('a', class_='tt').get_text()
        item['price_averages'] = float(
            soup.find('span', class_='red').get_text())
        for dd in dds:
            strong = dd.find('strong').get_text()
            if strong.strip() == '小区地址：':
                item['adress'] = dd.get_text().split('：')[-1]
            elif strong.strip() == '所属区域：':
                item['location'] = dd.get_text().split('：')[-1]
            elif strong.strip() == '产权描述：':
                item['right_descript'] = dd.get_text().split('：')[-1]
            elif strong.strip() == '建筑年代：':
                item['building_old'] = dd.get_text().split('：')[-1]
            elif strong.strip() == '物业类别：':
                item['neigh_type'] = dd.get_text().split('：')[-1]
            elif strong.strip() == '开 发 商：':
                item['developer'] = dd.get_text().split('：')[-1]
            elif strong.strip() == '建筑类别：':
                item['building_type'] = dd.get_text().split('：')[-1]
            elif strong.strip() == '建筑面积：':
                item['neigh_area'] = dd.get_text().split('：')[-1]
            elif strong.strip() == '占地面积：':
                item['building_area'] = dd.get_text().split('：')[-1]
            elif strong.strip() == '物业公司：':
                item['company'] = dd.get_text().split('：')[-1]
            elif strong.strip() == '绿 化 率：':
                item['green_rate'] = dd.get_text().split('：')[-1]
            elif strong.strip() == '容 积 率：':
                item['volumetric_rate'] = dd.get_text().split('：')[-1]
            elif strong.strip() == '物 业 费：':
                item['property_fee'] = dd.get_text().split('：')[-1]
            elif strong.strip() == '附加信息：':
                item['additional_info'] = dd.get_text().split('：')[-1]
         
        box = rate_box.find_all('dl')
        item['mid_month'] = box[0].get_text().strip().split('\n')[1]
        item['compare_month'] = box[1].get_text().strip().split('\n')[1]
        item['compare_year'] = box[2].get_text().strip().split('\n')[1]
        print(item)
        yield item

