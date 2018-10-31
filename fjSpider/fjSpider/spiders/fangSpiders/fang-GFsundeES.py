# -*-coding:utf-8-*-  
from re import search
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from scrapy import FormRequest, Request
from scrapy.spiders import Spider
from scrapy_splash import SplashRequest
from pyquery import PyQuery as pq
from fjSpider.items.fang_items import *
from lxml.html import etree

# 顺德小区房价信息


class fangSpider(Spider):
    name = 'fang-GFsundeES'
    url = 'http://esf.fs.fang.com/house-a0617/h316-i3%d-j3100/'
    flag = False
    custom_settings = {
        'ITEM_PIPELINES': {
            'fjSpider.pipelines.fang-pipelines.GFsundeESPipeline': 300,
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
    }

    def start_requests(self):

        for i in range(1, 2):
            if self.flag:
                break
            #ii js解析用splash
            yield SplashRequest(url=self.url % i, callback=self.parse, args={'wait': 0.5, 'html': 1})


    def parse(self, response):
        doc = pq(response.body.decode('utf8'))
        docs = pq(doc('.shop_list'))
        for i in docs('.floatl').items():
            link = 'http://fs.esf.fang.com'+ i('a').attr('href')
          # print(link)
        #link = 'http://fs.esf.fang.com/chushou/3_333943076.htm'
            yield SplashRequest(link, callback=self.second_parse)
    
    def second_parse(self, response):
        print(response.url) 
        item = GFsundeES_fangItem()
        item['url'] = response.url
        soup  = BeautifulSoup(response.body, 'lxml')
        item['title']  = soup.find('h1', class_='title floatl').get_text() 
        item['price_total'] =  soup.find('div', class_='trl-item_top').get_text().strip()
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
       # yield item

