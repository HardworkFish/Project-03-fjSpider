# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from scrapy.http import HtmlResponse
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.downloadermiddlewares.redirect import RedirectMiddleware
import random


class javascriptMiddleware(object):
    driver = webdriver.PhantomJS()
    print("PhantomJS is starting...")

    def process_request(self, request, spider):
        driver = self.driver
        if request.url.split('/')[-3] == 'house-a0617':
            driver.get(request.url)
            print(request.url)
            html = "" + driver.page_source
            return HtmlResponse(driver.current_url, body=html, encoding='utf-8', request=request)


class userAgentMiddleware(UserAgentMiddleware):

    def __init__(self, user_agent):
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user_agent=crawler.settings.get('MY_USER_AGENT'))

    def process_request(self, request, spider):
        agent = random.choice(self.user_agent)
        request.headers['User-Agent'] = agent

# class redirectMiddleware(RedirectMiddleware):
