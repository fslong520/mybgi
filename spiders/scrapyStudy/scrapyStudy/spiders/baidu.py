#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' baidu '

__author__ = 'fslong'

import scrapy


class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/']

    def start_requests(self):
        pass
        '''
        return [scrapy.FormRequest("http://www.baidu.com/",
                                   formdata={'username': 'john', 'pass': 'secret'},
                                   callback=self.logged_in)]
        '''

    def logged_in(self, response):
        # here you would extract links to follow and return Requests for
        # each of them, with another callback
        pass

    def parse(self, response):
        pass
