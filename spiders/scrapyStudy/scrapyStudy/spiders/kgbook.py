# -*- coding: utf-8 -*-
import pyquery
import requests
import scrapy
import re
from scrapyStudy.items import kgBookItem


class KgbookSpider(scrapy.Spider):
    lastpageNum = 1
    name = 'kgbook'
    allowed_domains = ['kgbook.com']
    start_urls = ['https://kgbook.com/list']
    bookId = 0
    url = 'https://kgbook.com/list'
    userAgent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'
    headers = {'User-Agent': userAgent, 'Connection': 'close', }
    req = requests.get(url, headers=headers, timeout=8)
    PQreq = pyquery.PyQuery(req.content.decode('utf-8'))
    pages = PQreq('.pagenavi a').items()
    lastpage = ''
    for i in pages:
        if i.text() == '尾页':
            lastpage = i.attr('href')
    if lastpage != '':
        lastpageNum = re.match(
            r'(https://kgbook.com/list/index_)(81)(.html)', lastpage).group(2)
        lastpageNum = int(lastpageNum)
    else:
        lastpageNum = 1
    lastpageNum = lastpageNum
    for i in range(lastpageNum):
        page = 'https://kgbook.com/list/index_'+str(i+1)+'.html'
        start_urls.append(page)

    def parse(self, response):
        bookName = response.xpath(
            '//div[@id="content"]/h1/text()').extract()
        column = response.xpath(
            '//div[@class="row collapse"]/nav[@class="breadcrumbs"]/a/text()').extract()
        link = []
        linkKey = response.xpath(
            '//div[@id="introduction"]/a/text()').extract()
        for i in range(len(linkKey)):
            link.append({linkKey[i]: response.xpath(
                '//div[@id="introduction"]/a/@href').extract()[i]})
        author = response.xpath(
            '//div[@id="news_details"]/ul/li/text()').extract()
        intro = response.xpath('//div[@id="introduction"]/p/text()').extract()
        # 使用生成器，一次又一次的返回items
        if bookName != []:
            self.bookId += 1
            items = kgBookItem()
            items['bookId'] = self.bookId
            items['bookName'] = bookName[0]
            items['column'] = column[0]
            items['author'] = author[0]
            items['intro'] = intro[0].replace(' ', '')
            items['link'] = link
            print(bookName)
            yield items

        for sel2 in response.xpath('//div[@class="channel-item"]/div[@class="bd"]/h3[@class="list-title"]'):
            for i in sel2.xpath('a/@href').extract():
                if i.startswith('http'):
                    url = i
                else:
                    url = 'https://kgbook.com'+i
                print(url)
                # 使用生成器返回一个request，然后再使用callback（回调函数）执行parse函数，
                yield scrapy.Request(url, callback=self.parse)


if __name__ == '__main__':
    book = KgbookSpider()
    print(book.start_urls)
