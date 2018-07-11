# -*- coding: utf-8 -*-
import scrapy


class DingdianSpider(scrapy.Spider):
    name = 'dingdian'
    allowed_domains = ['www.dingdiann.com']
    start_urls = ['http://www.dingdiann.com/']

    def parse(self, response):
        pass
