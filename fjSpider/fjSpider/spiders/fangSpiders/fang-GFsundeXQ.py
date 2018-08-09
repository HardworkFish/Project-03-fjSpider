# -*-coding:utf-8-*-  
from re import search
from urllib.parse import urljoin
import requests

from bs4 import BeautifulSoup
from scrapy import FormRequest, Request
from scrapy.spiders import Spider
from scrapy_splash import SplashRequest

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
        'DOWNLOAD_DELAY': 5,
    }

    def start_requests(self):
        for i in range(1, 70):
            # js解析用splash
            yield SplashRequest(self.url % i, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml', from_encoding='utf-8')
        dls = soup.find_all('dl', class_='plotListwrap clearfix')
        for dl in dls:
            url = dl.find('a', class_='plotTit')
            if url['href'][0] == '/':
                continue
            url = url['href'] + 'xiangqing/'
            item = GFsundeXQ_fangItem()
            item['house_age'] = dl.find('ul').find_all(
                'li')[-1].get_text().strip()
            yield Request(url, callback=self.second_parse, meta={'item': item})

    def second_parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml', from_encoding='utf-8')
        item = response.meta['item']
        dds = soup.find('div', class_='inforwrap clearfix').find_all('dd')
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
            elif strong.strip() == '物业类别：':
                item['neigh_type'] = dd.get_text().split('：')[-1]
            elif strong.strip() == '建筑类别：':
                item['building_type'] = dd.get_text().split('：')[-1]
            elif strong.strip() == '建筑面积：':
                item['neigh_area'] = dd.get_text().split('：')[-1]
            elif strong.strip() == '占地面积：':
                item['building_area'] = dd.get_text().split('：')[-1]
            elif strong.strip() == '容 积 率：':
                item['volumetric_rate'] = dd.get_text().split('：')[-1]
        if item.get('volumetric_rate', None) is not None or (item.get('neigh_area', None) is not None and item.get('building_area', None) is not None):
            yield SplashRequest(response.url.replace('xiangqing/', 'chushou/list/-h330-j3100/'), callback=self.third_parse, meta={'item': item})

    def third_parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml', from_encoding='utf-8')
        item = response.meta['item']
        ps = soup.find('div', class_='rentListwrap fangListwrap').find_all(
            'p', class_='mt5')
        total = 0
        count = 0
        for p in ps:
            try:
                # print(search('\\d+', p.get_text().strip().split(
                #     '|')[1].split('(')[-1]).group())
                total += int(search('\\d+', p.get_text().strip().split(
                    '|')[1].split('(')[-1]).group())
                count += 1
            except:
                continue
        item['total_floor'] = total / count
        yield item
