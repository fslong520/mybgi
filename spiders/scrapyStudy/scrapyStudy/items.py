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
    peopleName=scrapy.Field()
    intro=scrapy.Field()
    link=scrapy.Field()
    zuhe=scrapy.Field()

class kgBookItem(scrapy.Item):
    bookId=scrapy.Field()
    bookName = scrapy.Field()
    author = scrapy.Field()
    intro = scrapy.Field()
    column = scrapy.Field()
    link = scrapy.Field()

