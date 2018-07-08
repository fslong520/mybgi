#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' biquge '

__author__ = 'fslong'


import scrapy
import re
from scrapyStudy.items import ScrapystudyItem


class BiqugeSpider(scrapy.Spider):
    name = "biquge"
    allowed_domains = ["biquge.com.tw"]
    start_urls = ["http://www.biquge.com.tw/xuanhuan", ]

    def parse(self, response):
        for sel in response.xpath('//div[@class="l"]/ul/li'):
            bookName = sel.xpath('span[@class="s2"]/a/text()').extract()[0]
            link = sel.xpath('span[@class="s2"]/a/@href').extract()[0]
            column = sel.xpath('//div[@class="l"]/h2/text()').extract()[0]
            if re.match(r'好看的.*最近更新列表', column):
                column = re.match(r'(好看的)(.*)(最近更新列表)', column)[2]
                if column == '':
                    column = '最近更新小说列表'
            author = sel.xpath('span[@class="s5"]/text()').extract()[0]
            if re.match(r'(..)-(..)', author):
                author = sel.xpath('span[@class="s4"]/text()').extract()[0]
            # 使用生成器，一次又一次的返回items
            if bookName != []:
                items = ScrapystudyItem()
                items['column'] = column
                items['bookName'] = bookName
                items['author'] = author
                items['link'] = link
                print(bookName)
                yield items
        # 编写迭代，来获取各个栏目的书籍
        for sel2 in response.xpath('//div[@class="nav"]/ul/li'):
            for i in sel2.xpath('a/@href').extract():
                if i.startswith('http'):
                    pass
                else:
                    url = 'http://www.biquge.com.tw'+i
                    print(url)
                # 使用生成器返回一个request，然后再使用callback（回调函数）执行parse函数，
                yield scrapy.Request(url, callback=self.parse)
