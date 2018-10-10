# -*-coding:utf-8-*-  
from re import search
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from scrapy import FormRequest, Request
from scrapy.spiders import Spider
from scrapy_splash import SplashRequest

from fjSpider.items.fang_items import *

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
            # js解析用splash
            
            yield SplashRequest(url=self.url % i, callback=self.parse, args={'wait': 0.5, 'html': 1})
    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml', from_encoding='utf-8')
        url_lists = soup.find_all('span' , class_= 'tit_shop')
        print(url_lists)
        
#print(response.url)        
#print(soup)
        # 房源发布时间
        #updatedays = soup.find_all('span', class_='ml10 gray9')
        # 房源信息页面url
        #urls = soup.find('div', class_='houseList').find_all(
         #   'a', attrs={'title': ''})
        # print(response.url)
        # print(len(urls))
        #for url, updateday in zip(urls, updatedays):
            # 增量控制
            # 去除今天发布的房源
         #   if search('[小时分钟]+', updateday.get_text().strip()) != None:
          #      continue
            # 保留昨天发布的，去除其他的房源
           # elif updateday.get_text().strip()[:3] == '1天前':
                # print(updateday.get_text().strip())
            #    url = urljoin(response.url, url['href'])
             #   yield Request(url, callback=self.second_parse)
            #else:
             #   self.flag = True
              #  break
    

    def second_parse(self, response):
        # print('\n\n\n')
        soup = BeautifulSoup(response.body, 'lxml')

        item = GFsundeES_fangItem()
        item['url'] = response.url
        item['title'] = soup.find(
            'div', class_='title').get_text().strip().replace('\xa0', ' ')
        item['price_total'] = float(
            soup.find('div', class_='trl-item sty1').find('i').get_text())
        tts = soup.find_all('div', class_='tt')
        item['house_type'] = tts[0].get_text().strip()
        item['house_area'] = tts[1].get_text().strip()
        item['price_averages'] = tts[2].get_text().strip()
        item['house_towards'] = tts[3].get_text().strip()
        item['total_floor'] = soup.find_all('div', class_='trl-item1')[4].find_all(
            'div')[1].get_text().split('（')[-1].split('）')[0].strip()
        item['house_floor'] = tts[4].get_text().strip()
        item['decoration'] = tts[5].get_text().strip()
        blues = soup.find_all('a', class_='blue')
        if len(blues) == 2:
            item['neighborhood'] = response.xpath(
                '/html/body/div[5]/div[1]/div[3]/div[5]/div[1]/div[2]/text()')[0].extract().strip()
        else:
            item['neighborhood'] = blues[0].get_text().strip()
        item['location'] = blues[1].get_text().strip() + \
            blues[2].get_text().strip()
        infos = soup.find(
            'div', class_='cont clearfix qu_bianqu1').get_text().strip().replace('\n', ' ').split(' ')
        if infos[0] != '建筑年代':
            return
        for i, info in enumerate(infos):
            if info == '建筑年代':
                item['house_age'] = infos[i + 1]
            elif info == '产权性质':
                item['property_right'] = infos[i + 1]
            elif info == '住宅类别':
                item['residential_category'] = infos[i + 1]
            elif info == '建筑结构':
                item['structure'] = infos[i + 1]
            elif info == '建筑类别':
                item['construction_category'] = infos[i + 1]
            elif info == '挂牌时间':
                item['listed_time'] = infos[i + 1].split('(')[0]
        item['description'] = soup.find(
            'div', class_='mscont').get_text().strip()
        item['contact'] = soup.find(
            'span', id='agentname').get_text().strip()
        item['belong'] = soup.find_all(
            'div', class_='trlcont-line')[-1].find_all('span')[-1].get_text().strip()
        item['phone_number'] = soup.find(
            'span', class_='pnum').get_text().strip()
        yield item
