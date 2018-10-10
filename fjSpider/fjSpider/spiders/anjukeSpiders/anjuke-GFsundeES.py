# -*-coding:utf-8-*-  
from re import search

from bs4 import BeautifulSoup
from scrapy import Request
from scrapy.spiders import Spider

from fjSpider.items.anjuke_items import *


class anjukeSpider(Spider):
    name = 'anjuke-GFsundeES'
    url = 'https://foshan.anjuke.com/sale/shundequ/o5-p%d/'
    custom_settings = {
        'ITEM_PIPELINES': {
            'fjSpider.pipelines.anjuke-pipelines.anjukePipeline': 300,
        },

        # 下载器中间件
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'fjSpider.middlewares.userAgentMiddleware': 500,
        },
        'DOWNLOAD_DELAY': 10,
    }

    def start_requests(self):
        for i in range(1, 2):
            yield Request(self.url % i, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml', from_encoding='utf-8')
        #print("url:",soup)
        urls = soup.find(
            'ul', class_='houselist-mod houselist-mod-new').find_all('a')
        #print(urls)
        #print('urls:',urls)

        for url in urls:
            print(url['href'])
            yield Request(url['href'], callback=self.second_parse)


    def second_parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml', from_encoding='utf-8')
        item = anjukeItem()
        item['url'] = response.url.split('?')[0]
        item['title'] = soup.find('h3', class_='long-title').get_text().strip()
        item['price_total'] = float(
            soup.find('span', class_='light info-tag').find('em').get_text())
        code_string = soup.find(
            'span', class_='house-encode').get_text()
        item['house_code'] = code_string.split('：')[1].split('，')[0].strip()
        item['listed_time'] = code_string.split('：')[-1].strip()
        dds = soup.find(
            'ul', class_='houseInfo-detail-list clearfix').find_all('li')
        item['neighborhood'] = dds[0].get_text().strip()
        item['location'] = dds[1].get_text().strip().replace(
            '\n', '').replace(' ', '').replace('\ue003', '').replace('－', '')
        item['house_age'] = dds[2].get_text().strip()
        item['house_type'] = dds[3].get_text().strip()
        item['room_type'] = dds[4].get_text().strip().replace('\n',
                                                              '').replace(' ', '')
        item['house_area'] = dds[5].get_text().strip()
        item['house_towards'] = dds[6].get_text().strip()
        item['total_floor'] = dds[7].get_text().strip()
        item['decoration'] = dds[8].get_text().strip()
        item['price_averages'] =  dds[9].get_text().strip().replace('元/m\xb2', '').strip()
        item['description'] = soup.find(
            'div', class_='houseInfo-item-desc js-house-explain').get_text().strip()
        item['house_support'] = soup.find(
            'div', class_='houseInfo-item-desc').get_text()
        item['contact'] = soup.find(
            'div', class_='brokercard-name').get_text().strip()
        item['belong'] = soup.find(
            'i', class_='iconfont').get_text().replace(' ', '').strip()
        item['phone_number'] = soup.find(
            'div', class_='broker-company').get_text().strip()
        yield item

