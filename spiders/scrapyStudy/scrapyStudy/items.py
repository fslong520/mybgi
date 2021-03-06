# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapystudyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    bookName = scrapy.Field()
    author = scrapy.Field()
    intro = scrapy.Field()
    column = scrapy.Field()
    link = scrapy.Field()


class xueqiuItem(scrapy.Item):
    peopleName = scrapy.Field()
    intro = scrapy.Field()
    link = scrapy.Field()
    zuhe = scrapy.Field()


class kgBookItem(scrapy.Item):
    bookId = scrapy.Field()
    bookName = scrapy.Field()
    author = scrapy.Field()
    intro = scrapy.Field()
    column = scrapy.Field()
    link = scrapy.Field()


class DingDian(scrapy.Item):
    bookName = scrapy.Field()
    author = scrapy.Field()
    intro = scrapy.Field()
    column = scrapy.Field()
    link = scrapy.Field()

class NetbianItems(scrapy.Item):
    picId=scrapy.Field()
    clumnName=scrapy.Field()
    picName=scrapy.Field()
    picPreview=scrapy.Field()
    picSize=scrapy.Field()
    picUrl=scrapy.Field()
    picUpdateTime=scrapy.Field()
    picPage=scrapy.Field()


class Win4000Items(scrapy.Item):
    className=scrapy.Field()
    picId=scrapy.Field()
    clumnName=scrapy.Field()
    picName=scrapy.Field()
    picPreview=scrapy.Field()
    picSize=scrapy.Field()
    picNum=scrapy.Field()
    picUrl=scrapy.Field()
    picUpdateTime=scrapy.Field()
    allPicNum=scrapy.Field()