#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 雪球 '

__author__ = 'fslong'
import scrapy
from scrapyStudy.items import xueqiuItem


class XueqiuSpider(scrapy.Spider):
    name = 'xueqiu'
    allowed_domains = ['xueqiu.com']
    start_urls = ['https://xueqiu.com/people']

    def parse(self, response):
        for sel in response.xpath('//div[@class="cont desc_block"]/div[@class="info"]'):
            peopleName = sel.xpath('a[@class="name"]/@title').extract()
            intro = sel.xpath('a[@class="name"]/img/@title').extract()
            link=sel.xpath('a[@class="name"]/@href').extract()
            if intro!=[]:
                items=xueqiuItem()
                items['peopleName']=peopleName[0]
                items['intro']=intro[0]
                items['link']='https://xueqiu.com'+link[0]
                yield items
