#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Created on 2018-07-25 10:45:46
# Project: enterdesk

import json
import os
import re
import traceback

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    def __init__(self):
        self.baseUrlPC = 'https://www.enterdesk.com/zhuomianbizhi/'
        self.baseUrlMM = 'https://mm.enterdesk.com/'
        self.baseUrlMobile = 'https://sj.enterdesk.com/'
        self.pageNum = 1
        self.picId = 0
        self.pageClass = 0
        self.pic = {'pc': [], 'mm': [], 'mobile': [], }
        self.allPicNum = 0

    @every(minutes=24 * 60)
    def on_start(self):
        while self.pageNum <= 770:
            self.crawl(self.baseUrlPC+str(self.pageNum) +
                       '.html', callback=self.index_page)
            self.crawl(self.baseUrlMM+str(self.pageNum) +
                       '.html', callback=self.index_page)
            self.crawl(self.baseUrlMobile+str(self.pageNum) +
                       '.html', callback=self.index_page)
            self.pageNum += 1

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.egeli_pic_dl > dd > a').items():
            print(each.text())
            print(each.attr.href)
            self.crawl(each.attr.href, callback=self.detail_page1)

    @config(priority=2)
    def detail_page1(self, response):
        try:
            self.picId += 1
            column = []
            for each in response.doc('.arc_location > a').items():
                column.append(each.text())
            tag = []
            for each in response.doc('.myarc_tag > a').items():
                tag.append(each.text())
            picName = column[-1]
            picUrl = []
            picPreview = []
            picNum = 0
            print('当前网址是：%s' % response.url)
            if 'https://sj.enterdesk.com' in response.url:

                url = response.doc('.arc_main_pic > img').attr.src

                picPreview.append(url)

                url = 'https://up.enterdesk.com/edpic_source/' + \
                    url.split('https://up.enterdesk.com/edpic/')[-1]
                picNum += 1

                self.allPicNum += picNum
                picUrl.append(url)

                picSize = response.doc(
                    '.arc_top > .myarc_intro_span2 > a').text()

                picIntro = response.doc('.myarc_intro').text().split('内容简介')[1]
                print('匹配成功%s' % url)
                self.pic['mobile'].append({'picId': self.picId, 'picName': picName, 'picIntro': picIntro, 'picSize': picSize,
                                           'picUrl': picUrl, 'picPreview': picPreview, 'picColumn': column, 'picTag': tag, 'picNum': picNum, })
            else:
                picIntro = response.doc('.myarc_intro').text()
                picSize = response.doc('.arc_top .myarc_intro_span2').text()
                for each in response.doc('.swiper-wrapper img').items():
                    url = each.attr.src
                    picPreview.append(url)
                    url = 'https://up.enterdesk.com/edpic_source/' + \
                        url.split('/edpic_360_360/')[-1]
                    picNum += 1
                    picUrl.append(url)

                if 'https://www.' in response.url:
                    self.allPicNum += picNum
                    self.pic['pc'].append({'picId': self.picId, 'picName': picName, 'picIntro': picIntro, 'picSize': picSize,
                                           'picUrl': picUrl, 'picPreview': picPreview, 'picColumn': column, 'picTag': tag, 'picNum': picNum, })
                else:
                    self.allPicNum += picNum
                    self.pic['mm'].append({'picId': self.picId, 'picName': picName, 'picIntro': picIntro, 'picSize': picSize,
                                           'picUrl': picUrl, 'picPreview': picPreview, 'picColumn': column, 'picTag': tag, 'picNum': picNum, })

            print(column)
            print(tag)
            print(picUrl)
            with open('/mnt/c/Users/fengs/OneDrive/Documents/Projects/mybgi/spiders/pyspider/enterdesk.json', 'w', encoding='utf-8') as f:
                json.dump(self.pic, f, ensure_ascii=False)
            return {'picId': self.picId, 'picName': picName, 'picIntro': picIntro, 'picSize': picSize, 'picUrl': picUrl, 'picPreview': picPreview, 'picColumn': column, 'picTag': tag, 'picNum': picNum, 'allPicNum': self.allPicNum, }
        except:
            traceback.print_exc()

    '''# 示例
        for each in response.doc('a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }
    '''


if __name__ == '__main__':
    path = os.path.dirname(__file__)
    # 用于处理pyspider导出的json
    with open(os.path.join(path, 'enterdesk12.json'), 'r', encoding='utf-8') as f:
        lines = f.read().split('{"taskid"')
        jsonStr = '['
        for line in lines:
            if line == '':
                pass
            else:
                jsonStr += '{"taskid"'+line+','
        # 去除一些没用的字符串
        jsonStr = jsonStr[0:-1]+']'
        jsonStr = jsonStr.replace(' ', '')
        jsonStr = jsonStr.replace('\n', '')
        jsonStr = jsonStr.replace('\t', '')
        jsonStr = jsonStr.replace('\r', '')
        # print(jsonStr)
        picDict = json.loads(jsonStr, encoding='utf-8')
        allPicNum = 0
        for i in picDict:
            i['result']['picSize'] = i['result']['picSize'].split('查看')[0]
            i['result'].pop('allPicNum')
            allPicNum += i['result']['picNum']

    with open(os.path.join(path, 'enterdesk123.json'), 'w', encoding='utf-8') as f:
        json.dump(picDict, f, ensure_ascii=False)
