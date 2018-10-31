# -*-coding:utf-8-*-  
from re import search
from urllib.parse import urljoin
import requests
from time import sleep
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
from scrapy import FormRequest, Request
from scrapy.spiders import Spider
from scrapy_splash import SplashRequest

from fjSpider.items.fang_items import *

# 深圳房价信息


class GSZESSpider(Spider):
    name = 'fang-GSZES'
    url = 'http://esf.sz.fang.com/house/h316-i3%d-j3100/'
    custom_settings = {
        'ITEM_PIPELINES': {
            'fjSpider.pipelines.fang-pipelines.GDSZESPipeline': 300,
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
        'DOWNLOAD_DELAY': 4,
    }

    def start_requests(self):
        for i in range(1, 2):
            # js解析用splash
            yield SplashRequest(self.url % i, callback=self.parse, dont_filter=True)

    def parse(self, response):
        doc = pq(response.body.decode('utf8'))
        docs = pq(doc('.shop_list'))
        #print(docs('float1').items()) 
        for i in docs('.floatl').items():
            link = 'http://sz.esf.fang.com'+i('a').attr('href')
            yield SplashRequest(link, callback=self.second_parse)

    def second_parse(self, response):
        print(response.url) 
        item = GFsundeES_fangItem()
        item['url'] = response.url
        soup  = BeautifulSoup(response.body, 'lxml')
        item['title']  = soup.find('h1', class_='title floatl').get_text() 
        item['price_total'] =  soup.find('div', class_='price_esf').get_text().strip()
        tts = soup.find_all('div', class_='tt')
        item['house_type'] = tts[0].get_text().strip()
        item['house_area'] = tts[1].get_text().strip()
        item['price_averages'] = tts[2].get_text().strip()
        item['house_towards'] = tts[3].get_text().strip()
        item['total_floor'] = soup.find_all('div', class_='trl-item1')[4].find_all(
            'div')[1].get_text().split('（')[-1].split('）')[0].strip()
        item['house_floor'] = tts[4].get_text().strip()
        item['decoration'] = tts[5].get_text().strip()
      #  print(item)        
        infos = soup.find_all(
            'span', class_='rcont')
       # print(infos[0].get_text().strip())
        #print(infos)
        item['house_age'] = infos[0].get_text().strip()
        item['property_right'] = infos[1].get_text().strip()
        item['residential_category'] = infos[2].get_text().strip()
        item['structure'] = infos[3].get_text().strip()
        item['construction_category'] = infos[4].get_text().strip()
        item['listed_time'] = infos[5].get_text().strip()
        #print(item) 
        item['description'] = soup.find('li', class_='font14 hxmd').get_text().strip()
        item['contact'] = soup.find(
            'span', id='mobilecode').get_text().strip()
        item['belong'] = soup.find(
            'span', class_='zf_jjname').get_text().strip()
        print(item)
        yield item
