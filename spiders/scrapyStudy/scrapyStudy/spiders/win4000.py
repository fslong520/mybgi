# -*- coding: utf-8 -*-
import traceback

import scrapy

from scrapyStudy.items import Win4000Items


class Win4000Spider(scrapy.Spider):
    name = 'win4000'
    allowed_domains = ['win4000.com']
    start_urls = [
                  'http://www.win4000.com/wallpaper_191_0_0_1.html', 
                  'http://www.win4000.com/wallpaper_192_0_0_1.html', 
                  'http://www.win4000.com/wallpaper_193_0_0_1.html', 
                  'http://www.win4000.com/wallpaper_194_0_0_1.html', 
                  'http://www.win4000.com/wallpaper_195_0_0_1.html', 
                  'http://www.win4000.com/wallpaper_196_0_0_1.html', 
                  'http://www.win4000.com/wallpaper_197_0_0_1.html', 
                  'http://www.win4000.com/wallpaper_198_0_0_1.html', 
                  'http://www.win4000.com/wallpaper_199_0_0_1.html', 
                  'http://www.win4000.com/wallpaper_200_0_0_1.html', 
                  'http://www.win4000.com/wallpaper_201_0_0_1.html', 
                  'http://www.win4000.com/wallpaper_202_0_0_1.html', 
                  'http://www.win4000.com/wallpaper_203_0_0_1.html', 
                  'http://www.win4000.com/wallpaper_204_0_0_1.html', 
                  'http://www.win4000.com/wallpaper_205_0_0_1.html', 
                  'http://www.win4000.com/wallpaper_206_0_0_1.html',                   
                  'http://www.win4000.com/wallpaper_207_0_0_1.html',                   
                  'http://www.win4000.com/wallpaper_208_0_0_1.html',                   
                  'http://www.win4000.com/wallpaper_209_0_0_1.html',                   
                  'http://www.win4000.com/wallpaper_2285_0_0_1.html',                  
                  'http://www.win4000.com/wallpaper_2286_0_0_1.html',                  
                  'http://www.win4000.com/wallpaper_2287_0_0_1.html',                  
                  'http://www.win4000.com/wallpaper_2357_0_0_1.html',                   
                  'http://www.win4000.com/wallpaper_2358_0_0_1.html',                   
                  'http://www.win4000.com/wallpaper_2361_0_0_1.html',  
                  'http://www.win4000.com/mobile_2359_0_0_1.html',  
                  'http://www.win4000.com/mobile_2360_0_0_1.html',  
                  'http://www.win4000.com/mobile_2362_0_0_1.html']
    i=2338
    while i<=2356:
        start_urls.append('http://www.win4000.com/mobile_'+str(i)+'_0_0_1.html')
        i+=1
    pageNum = 1
    picId = 0
    allPicNum = 0

    # 解析除首页外详细页

    def detailParse2(self, response):
        # 获取上层解析过的数据
        items = response.meta['items']
        nowNum = response.meta['nowNum']
        picNum = response.meta['picNum']
        nowPicUrl = response.xpath(
            '//div[@class="col-main"]/div/div/a/img/@src').extract()[0]
        items['picPreview'].append(nowPicUrl[0:-4]+'_250_350.jpg')
        items['picUrl'].append(nowPicUrl)
        if nowNum == picNum:
            print('现在的图片是：%s' % items['picName'])
            print('现在一共获取了%s张图片。' % self.allPicNum)
            yield items

    # 解析详细页（首页）：

    def detailParse1(self, response):
        # 获取上层解析过的数据
        items = response.meta['items']
        items['picPreview'] = []
        items['picUrl'] = []
        className = response.xpath(
            '//div[@class="main"]/div[@class="main_cont"]/div/a/text()').extract()[1]
        clumnName = response.xpath(
            '//div[@class="main"]/div[@class="main_cont"]/div/a/text()').extract()[2]
        picUpdateTime = response.xpath(
            '//div[@class="pic_main"]/div/div/div[@class="Bigimg_style"]/span[@class="time"]/text()').extract()[0]
        picSize = response.xpath(
            '//div[@class="pic_main"]/div/div/div[@class="Bigimg_style"]/span[@class="size"]/em/text()').extract()[0]
        nowPicUrl = response.xpath(
            '//div[@class="col-main"]/div/div/a/img/@src').extract()[0]
        items['picPreview'].append(nowPicUrl[0:-4]+'_250_350.jpg')
        items['picUrl'].append(nowPicUrl)
        self.picId += 1
        items['picId'] = self.picId
        items['className'] = className
        items['clumnName'] = clumnName
        items['picUpdateTime'] = picUpdateTime
        items['picSize'] = picSize
        picNum = int(response.xpath(
            '//div[@class="ptitle"]/em/text()').extract()[0])
        items['picNum'] = picNum
        self.allPicNum += picNum
        for i in range(picNum-1):
            picUrlDetailNext = str(response.url).split('.html')[
                0]+'_'+str(i+2)+'.html'
            print('\n图片详细页的网址：%s\n' % picUrlDetailNext)
            yield scrapy.Request(picUrlDetailNext, meta={'items': items, 'picNum': picNum, 'nowNum': i+2}, callback=self.detailParse2)

    # 主体解析函数：

    def parse(self, response):
        for i in response.xpath('//div[@class="main_cont"]/div[@class="w1180 clearfix"]/div/div/div/div/div/ul/li'):
            items = Win4000Items()
            picName = i.xpath('a/p/text()').extract()[0]
            print('\n%s\n' % picName)
            picUrlDetail = i.xpath('a/@href').extract()[0]
            items['picName'] = picName
            yield scrapy.Request(picUrlDetail, meta={'items': items}, callback=self.detailParse1)

        # 翻页：
        if self.pageNum <= 100000:
            print('\n页码:%s\n' % self.pageNum)
            nextPageUrl = response.xpath(
                '//div[@class="pages"]/div/a[@class="next"]/@href').extract()[0]
            self.pageNum += 1
            print('\n下一页的网址:%s\n' % nextPageUrl)
            yield scrapy.Request(nextPageUrl, callback=self.parse)
