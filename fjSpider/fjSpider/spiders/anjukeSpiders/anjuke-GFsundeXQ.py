# -*-coding:utf-8-*-  
from scrapy.spiders import Spider
from scrapy import Request
from bs4 import BeautifulSoup
from fjSpider.items.anjuke_items import GFsundeXQ_anjukeItem
from urllib.parse import urljoin
from collections import deque
import urllib
class anjukeSpider(Spider):
    name='anjuke-GFsundeXQ'
    url = 'https://foshan.anjuke.com/community/shundequ/o6-p%d/'
    price_average = deque()
    price_rate = deque()
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
        for i in range(1):#50
            yield Request(self.url%(i+1),callback=self.parse)

    def parse(self,response):
        soup = BeautifulSoup(response.body,'lxml',from_encoding='utf-8')
        divs = soup.find_all('div',class_='li-itemmod')
       # prices = divs.find('div', class_='li-side')
       # for price in prices:
            #print(price.get_text())
        for div in divs:
            price_list = div.find('div', class_='li-side').find_all('p')
            #self.price_average.append(price_list[0].get_text().strip())
            #self.price_rate.append(price_list[1].get_text().strip())
            #print(price_list[1].get_text())
           # print(div['link'])
            price_average = price_list[0].get_text().strip()
            price_rate = price_list[1].get_text().strip()

            link=urljoin(response.url,div['link'])

      #self.price_average = self.price_average.reverse()
       # self.price_rate = self.price_rate.reverse()

    def second_parse(self,response):
        price_rate = response.meta['price_rate']
        price_average = response.meta['price_average']
        #self.url
        url = response.url
        soup = BeautifulSoup(response.body, 'lxml', from_encoding='utf-8')
        item = GFsundeXQ_anjukeItem()
        item['url'] = response.url.split('?')[0]
        item['neighborhood'] = soup.find('h1').get_text().strip()
        item['location'] = soup.find('h1').find('span').get_text()

        code_string = soup.find(
            'div',class_='basic-infos-box')

        dds = code_string.find(
            'dl', class_='basic-parms-mod').find_all('dd')
        item['neigh_type'] = dds[0].get_text()
        item['neigh_price'] = dds[1].get_text()
        item['neigh_area_total'] = dds[2].get_text()
        item['neigh_user_total'] = dds[3].get_text()
        item['building_time'] = dds[4].get_text()
        item['neigh_parting'] = dds[5].get_text()
        item['volumetric_rate'] = dds[6].get_text()
        item['green_rate'] = dds[7].get_text()
        item['neigh_developer'] = dds[8].get_text()
        item['neigh_company'] = dds[9].get_text()
        item['price_average'] = price_average
        item['price_rate'] = price_rate
       # url_id = url.split('/')[0]
       # print(url_id)
        #price_url ="https://foshan.anjuke.com/community_ajax/478/price/?cis=%s" % url_id
        yield item


###差一个平均价格
