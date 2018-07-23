# -*- coding: utf-8 -*-
import scrapy
import requests
import pyquery
from scrapyStudy.items import NetbianItems


class NetbianSpider(scrapy.Spider):
    name = 'netbian'
    allowed_domains = ['www.netbian.com']
    start_urls = ['http://www.netbian.com/']
    count = 0
    picId = 0

    def urlCompleting(self, url):
        if url.startswith('http'):
            return url
        else:
            url = 'http://www.netbian.com'+url
            return url

    # 解析第一层图片详情：
    def detailParse1(self, response):
        # 接收上级已爬取的数据
        item = response.meta['item']
        clumnName = response.xpath(
            '//div[@class="action"]/a/text()').extract()[1]
        picSize = response.xpath(
            '//div[@class="pic-down"]/a/span/text()').extract()[0]
        item['picSize'] = picSize[1:-1]
        item['clumnName'] = clumnName
        picUrl2 = response.xpath(
            '//div[@class="pic-down"]/a/@href').extract()[0]
        picUrl2 = self.urlCompleting(picUrl2)
        yield scrapy.Request(picUrl2, meta={'item': item}, callback=self.detailParse2)

    # 解析第二层图片详情：

    def detailParse2(self, response):
        # 接收上级已爬取的数据
        item = response.meta['item']
        picUrl = response.xpath(
            '//td[@align="left"]/a/img/@src').extract()[0]
        item['picUrl'] = picUrl
        self.picId += 1
        item['picId'] = self.picId
        yield item

    def parse(self, response):
        # 解析获取缩略图：
        for i in response.xpath('//div[@id="main"]/div[@class="list"]/ul/li'):
            try:
                picName = i.xpath('a/@title').extract()[0]
                picUrl1 = i.xpath('a/@href').extract()[0]
                picUrl1 = self.urlCompleting(picUrl1)
                picPreview = i.xpath('a/img/@src').extract()[0]
                picUpdateTime = i.xpath('p/text()').extract()[0]
                item = NetbianItems()
                item['picId'] = 0
                item['picName'] = picName
                item['picPreview'] = picPreview
                item['picUpdateTime'] = picUpdateTime
                item['picPage']=self.count
                yield scrapy.Request(picUrl1, meta={'item': item}, callback=self.detailParse1)
            except:
                pass

        # 翻页：
        nextPageUrl = response.xpath(
            '//div[@class="page"]/a[@class="prev"]/@href').extract()
        print('下一页：%s' % nextPageUrl)
        if nextPageUrl != []:
            # 有上一页有后一页，想了想还是直接用最后一页吧！
            nextPageUrl = nextPageUrl[::-1]
            url = self.urlCompleting(nextPageUrl[0])
            print('网址：%s' % url)
            self.count += 1
            # 使用生成器返回一个request，然后再使用callback（回调函数）执行parse函数，
            yield scrapy.Request(url, callback=self.parse)
