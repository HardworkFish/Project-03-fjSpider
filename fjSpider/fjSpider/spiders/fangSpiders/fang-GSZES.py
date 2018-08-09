# -*-coding:utf-8-*-  
from re import search
from urllib.parse import urljoin
import requests
from time import sleep

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
        'SPLASH_URL': 'http://192.168.99.100:8050',

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
        for i in range(1, 100):
            # js解析用splash
            yield SplashRequest(self.url % i, callback=self.parse, dont_filter=True)

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml', from_encoding='utf-8')
        dls = soup.find_all('dl', class_='list rel')
        for dl in dls:
            try:
                item = GDSZES_fangItem()
                item['url'] = urljoin(response.url, dl.find('a')['href'])
                item['price_avg'] = int(
                    dl.find('p', class_='danjia alignR mt5').get_text()[:-3])
                item['location'] = dl.find(
                    'span', class_='iconAdress ml10 gray9').get_text()
                yield item
            except:
                continue
