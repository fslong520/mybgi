
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' wallpapersite.com爬虫 '

__author__ = 'fslong'


import ast
import json
import multiprocessing
import os
import re
import threading
import time
import traceback

import pyquery
import requests
import random


class Wallpapersite(object):
    def __init__(self):
        self.path = os.path.dirname(__file__)
        self.url = 'https://wallpapersite.com'
        self.userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17704'
        self.headers = {'User-Agent': self.userAgent, }
        self.num = 0
        self.pics = {}

    def getpages(self):
        req = requests.get(self.url, headers=self.headers, timeout=20)
        PQreq = pyquery.PyQuery(req.content)
        for i in PQreq('.pages > a').items():
            if 'Next' not in i.text():
                pages = i.text()
        self.getPic(PQreq, 1)
        try:
            pages = int(pages)
            self.pages = pages
        except:
            traceback.print_exc()

    def getPic(self, PQreq, page):
        # 使用多线程爬取网页上的照片:
        print('\n------------------\n开始下载第%s页数据\n------------------' % page)

        def loop(PQreq):
            j = 0
            for i in PQreq('#pics-list > p').items():
                htmlUrl = self.url+i('a').attr.href
                req = requests.get(htmlUrl, headers=self.headers, timeout=20)
                PQreq = pyquery.PyQuery(req.content)
                column = PQreq('.inner .main').text().split(' /')[0]
                name = PQreq('.inner .sub').text().split(' / ')[-1][2:]
                tags = []
                for i in PQreq('.tags > a').items():
                    tags.append(i.text())
                url = []
                print(name)
                for i in PQreq('.res-ttl a').items():
                    size = i.text().split('(')[1][0:-1]
                    url.append({'size': size, 'url': self.url+i.attr.href})
                    # print('pic'+str(j+1))
                    self.pics['pic'+str(j+1)] = {'picColumn': column,
                                                 'picName': name, 'picTag': tags, 'picUrl': url}
                    j += 1
                self.num += 1
                # 为防止被和谐，随机睡眠一段时间
                #time.sleep(5*random.random())
        t = threading.Thread(target=loop, name='LoopThread', args=(PQreq,))
        t.start()
        t.join()
        print('------------------\n第%s页数据下载完毕\n------------------\n' % page)       
        return {'num': self.num, 'data': self.pics}
        # print(self.pics)

    def getPicByPages(self, page, picsDict):
        req = requests.get(self.url+'?page='+str(page),
                           headers=self.headers, timeout=20)
        PQreq = pyquery.PyQuery(req.content)
        picsDict['page'+str(page)] = self.getPic(PQreq, page)
          


if __name__ == '__main__':
    picsDict = multiprocessing.Manager().dict()
    wallpapersite = Wallpapersite()
    wallpapersite.getpages()
    picsDict['page1'] = {'num': wallpapersite.num, 'data': wallpapersite.pics}
    try:
        start = time.time()
        i = 0  # 进程数
        # 多进程方法
        pages = wallpapersite.pages
        #pages = 2 # 用于测试
        # 由于一次性生成的进程太多的话会炸掉，所以每次只生成20个进程。
        m = int(pages/20)
        n = pages % 20
        for l in range(m):
            p = multiprocessing.Pool(20)
            for q in range(20):
                if 20*l+q == 0:
                    pass
                else:
                    i += 1
                    wallpapersiteTemp = Wallpapersite()
                    p.apply_async(wallpapersiteTemp.getPicByPages,
                                  args=(20*l+q, picsDict))                    
            p.close()
            p.join()
        p = multiprocessing.Pool(4)
        for l in range(n):
            if l == n-1:
                pass
            else:
                i += 1
                wallpapersiteTemp = Wallpapersite()
                p.apply_async(wallpapersiteTemp.getPicByPages,
                              args=(pages-l, picsDict))               
        p.close()
        p.join()
        # print(picsDict)
        
    except:
        traceback.print_exc()
    finally:
        with open(os.path.join(wallpapersite.path, 'wallpapersite.json'), 'w', encoding='utf-8') as f:
            dictStr = str(picsDict)
            dictForJson = ast.literal_eval(dictStr)
            json.dump(dictForJson, f, ensure_ascii=False)
        numAll = 0
        for i in dictForJson:
            numAll += picsDict[i]['num']
        print('一共%s张照片' % numAll)
        end = time.time()
        print('\n-----------------------\n下载了%s页数据，一共执行了 %0.2f seconds.\n' %
              (pages,(end - start)))
