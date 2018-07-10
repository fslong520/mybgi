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
    peoples=[]

    def parse(self, response):
        for sel0 in response.xpath('//div[@class="desc_block"]'):
            for i in sel0.xpath('a/@href').extract():
                if i.startswith('http'):
                    url = i
                else:
                    url = 'https://xueqiu.com'+i
                print(url)
                # 使用生成器返回一个request，然后再使用callback（回调函数）执行parse函数，
                yield scrapy.Request(url, callback=self.parse)

        peopleName = response.xpath('//div[class="profiles__hd__info"]/h2/text()').extract()
        intro = response.xpath('//div[class="profiles__hd__info"]/p/text()').extract()            
        if peopleName != []:
            items = xueqiuItem()
            items['peopleName'] = peopleName[0]
            items['intro'] = intro[0]
            items['link'] = response.url()
            yield items
            
# 雪球有个自动跳转，比较难处理；

if __name__ == '__main__':
    peoples = XueqiuSpider()
