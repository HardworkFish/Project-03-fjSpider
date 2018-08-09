from scrapy.spiders import Spider
from scrapy import Request, FormRequest
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from re import findall
from fjSpider.items.sofang_items import *
from datetime import *


class exampleSpider(Spider):

    name = 'sofang'
    url = 'http://fs.sofang.com/esfsale/area/aa1190-bl%d'

    custom_settings = {
        'ITEM_PIPELINES': {
            'fjSpider.pipelines.sofang-pipelines.sofangPipeline': 300,
        },
#
        # 下载器中间件
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'fjSpider.middlewares.userAgentMiddleware': 500,
        },
        'DOWNLOAD_DELAY': 10,
    }

    def start_requests(self):#21
        print("###############################################")
        for pagenum in range(1, 2):
            print("###############################################")
            yield Request(url=self.url % pagenum, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        a_list = soup.find_all('dt')
        for a in a_list:
            url = urljoin(response.url, a.find('a')['href'])
            print(url)
            yield Request(url=url, callback=self.second_parse)

    def second_parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        item = sofangItem()
        #item['house_name'] = soup.find('p', class_='house_name').get_text()
        print(soup.find('p', class_='house_name'))
        time = soup.find('p', class_='house_time').get_text()
        if len(time.split('：')) == 2:
            item['house_time'] = time.split('：')[-1]
        else:
            delta = int(findall('\\d+', time)[0])
            item['house_name'] = datetime.strftime(
                datetime.now() - timedelta(delta), '%Y年%m月%d日')
        item['house_tag'] = []
        for span in soup.find('p', class_='house_tge').find_all('span'):
            item['house_tag'].append(span.get_text())
        item['price_total'] = soup.find('p', class_='total').get_text()
        item['price_averages'] = soup.find('p', class_='averages').get_text()
        div = soup.find('div', class_='info')
        dts = div.find_all('dt')
        dds = div.find_all('dd')
        item['house_pattern'] = dts[0].get_text()
        item['house_area'] = dts[1].get_text()
        item['house_towards'] = dts[2].get_text()
        item['house_floor'] = dds[0].get_text()
        item['house_type'] = dds[1].get_text()
        item['house_age'] = dds[2].get_text()
        item['property_name'] = soup.find('a', class_='colorR').get_text()
        item['location'] = soup.find(
            'span', class_='address color0').get_text().replace(' ', '')
        item['position_x'] = soup.find('li', class_='no_float').find_all('a')[
            1]['href'].split('=')[-2].split('&')[0]
        item['position_y'] = soup.find('li', class_='no_float').find_all('a')[
            1]['href'].split('=')[-1]
        item['description'] = soup.find(
            'div', class_='depict').get_text().strip()
        yield item
