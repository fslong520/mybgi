# -*- coding: utf-8 -*-
import scrapy


class BiquduSpider(scrapy.Spider):
    name = 'biqudu'
    allowed_domains = ['biqudu.com']
    start_urls = ['https://biqudu.com/']

    def parse(self, response):
        pass
