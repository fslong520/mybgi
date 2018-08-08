#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 使用百度的高级搜索去查找上市公司一定时期内的新闻数量，从而判断上市公司近期的热度 '

__author__ = 'fslong'

import ast
import asyncio
import json
import os
import pickle
import re
import threading
import time
import traceback
from multiprocessing import Manager, Pool, Queue

import jieba
import pyquery
import requests
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render

import matplotlib.pyplot as plt
from wordcloud import STOPWORDS, ImageColorGenerator, WordCloud


class BaiduSearch(object):
    def __init__(self):
        self.searchKey = ''
        self.path = os.path.dirname(os.path.dirname(__file__))
        self.url = 'https://www.baidu.com/s'
        self.searchUrl = {'weibo': 'weibo.com',
                          'xueqiu': 'xueqiu.com', }
        self.timeQuantum = {'day': 24*60*60, 'week': 7*24 *
                            60*60, 'month': 30*24*60*60, 'year': 365*24*60*60, }
        self.userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17704'
        self.headers = {'User-Agent': self.userAgent, }
        self.cookies = {
            'Cookie': 'ispeed_lsm=2; BD_UPN=1d314753; BD_CK_SAM=1; sug=3; sugstore=1; ORIGIN=0; bdime=0; H_PS_645EC=7a4eVyZxpP0XlcUIo0qEEWNyE2iYbGSdOQUYCEW7wSYw36D94S0%2Fu9j4kL86TvQ; BDSVRTM=172; WWW_ST=1532662392353; BAIDUID=6E1A0F5F897FF29C1B26BC86F5363786:FG=1; BIDUPSID=79C7A5EE0EC2060E7C76882EB70E00F0; PSTM=1525936371; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; MCITY=-48%3A; BDUSS=lFZYzRBeERzUWVKbGlObFB5SXlnM2hoVFlYbVBYMURRVEVKNX5OWmREZ1dFVjFiQVFBQUFBJCQAAAAAAAAAAAEAAABmZwwOZnNsNDcwNjU3NTcwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABaENVsWhDVbU; BDRCVFR[fBLL8ZbbiMm]=mk3SLVN4HKm; PSINO=7; H_PS_PSSID=26523_1423_26908_21083_26350_20929'}
        self.num = 0
        self.news = []
    # 根据给定参数返回搜索用的时间段,timeQuantum单位是秒:

    def getSearchTimeQuantum(self, timeQuantum):
        nowTime = '%0.3f' % time.time()
        oldTime = '%0.3f' % (time.time()-timeQuantum)
        return [oldTime, nowTime]

    # 获取百度网页的数据:
    def getWebsiteDate(self, timeQuantumKey, searchUrlKey, searchKey):
        timeQuantum = self.getSearchTimeQuantum(
            self.timeQuantum[timeQuantumKey])
        searchUrl = self.searchUrl[searchUrlKey]
        params = {'q1': searchKey,
                  'q2': '',
                  'q3': '',
                  'q4': '',
                  'gpc': 'stf='+timeQuantum[0]+','+timeQuantum[1]+'|stftype%=1',
                  'ft': '',
                  'q5': '',
                  'q6': searchUrl,
                  'tn': 'baiduadv'}
        url = self.url
        req = requests.get(
            url, params=params, headers=self.headers, cookies=self.cookies, timeout=20)
        # print(req.url)
        PQreq = pyquery.PyQuery(req.text)
        print(
            '\n-----------------------\n开始下载<%s>的数据：\n-----------------------\n' % searchKey)
        # print('\n首先获取第1页数据：')
        for i in PQreq('.c-container').items():
            self.num += 1
            print('第%s条资讯：%s' % (self.num, i('h3 a').text()))
            print(i('.c-abstract').text())
            self.news.append({'news': i('h3 a').text(), 'url': i(
                'h3 a').attr.href, 'intro': i('.c-abstract').text()})
        # print('第1页数据下载完毕：')
        for i in PQreq('#page > a').items():
            if '下一页' in i.text():
                self.parseWebsiteDate(i.attr.href)
        print('数据获取完毕')

    def parseWebsiteDate(self, url):
        url = 'https://www.baidu.com'+url
        req = requests.get(url, headers=self.headers,
                           cookies=self.cookies, timeout=20).text
        PQreq = pyquery.PyQuery(req)
        # nowPage = PQreq('#page > strong > .pc')
        #print('开始获取第%s页数据：' % nowPage.text())

        async def parseNews():
            for i in PQreq('.c-container').items():
                self.num += 1
                print('第%s条资讯：%s' % (self.num, i('h3 a').text()))
                print(i('.c-abstract').text())
                self.news.append({'news': i('h3 a').text(), 'url': i(
                    'h3 a').attr.href, 'intro': i('.c-abstract').text()})
        for i in PQreq('#page > a').items():
            if '下一页' in i.text():
                self.parseWebsiteDate(i.attr.href)
        loops = asyncio.get_event_loop()
        tasks = [parseNews()]
        loops.run_until_complete(asyncio.wait(tasks))
        loops.close()
        #print('数据获取完毕' % nowPage.text())


def chirldProcess(key, baiduSearch):
    baiduSearchIn = BaiduSearch()
    baiduSearchIn.getWebsiteDate('day', 'xueqiu', key[0])
    if baiduSearchIn.num > 0:
        baiduSearch[key[0]] = {'num': baiduSearchIn.num,
                               'news': baiduSearchIn.news, }
        # json.dump(baiduSearch, f, ensure_ascii=False)


if __name__ == '__main__':
    a = input('获取还是分析数据(g/a)？')
    if a == 'g':
        # 建立一个用于主进程与子进程通信的字典：
        baiduSearch = Manager().dict()
        try:
            start = time.time()
            i = 0
            # 多进程方法
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static/stockAnalysis/json/stocklistTest.json'), 'r', encoding='utf-8')as f:
                stockListInfile = json.load(f)
                stockList = stockListInfile['sh']
                stockList[0:0] = stockListInfile['sz']
            stockLen = len(stockList)
            # 由于一次性生成的进程太多的话会炸掉，所以每次只生成20个进程。
            m = int(stockLen/20)
            n = stockLen % 20
            for l in range(m):
                p = Pool(20)
                for q in range(20):
                    i += 1
                    #print('生成第%s个进程' % i)
                    #print('第%s次遍历' % str(l+1))
                    p.apply_async(chirldProcess, args=(
                        stockList[20*l+q], baiduSearch))
                p.close()
                p.join()
            p = Pool(4)
            for q in range(n):
                if n == 0:
                    pass
                else:
                    i += 1
                    print('生成第%s个进程' % i)
                    p.apply_async(chirldProcess, args=(
                        stockList[-q], baiduSearch))
            p.close()
            p.join()

            # 等子进程执行完之后再存储数据：
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static/stockAnalysis/json/baidu.json'), 'w', encoding='utf-8')as f:
                dictStr = str(baiduSearch)
                dictForJson = ast.literal_eval(dictStr)
                json.dump(dictForJson, f, ensure_ascii=False)

            '''
            # 多线程方法
            def loop(i):
                for key in [["浦发银行", "SH600000"], ["邯郸钢铁", "SH600001"], ["齐鲁石化", "SH600002"], ["ST东北高", "SH600003"], ["白云机场", "SH600004"], ["武钢股份", "SH600005"], ["东风汽车", "SH600006"], ["中国国贸", "SH600007"], ["首创股份", "SH600008"], ["上海机场", "SH600009"], ["包钢股份", "SH600010"], ["华能国际", "SH600011"], ["皖通高速", "SH600012"], ["华夏银行", "SH600015"], ["民生银行", "SH600016"], ]:
                    i+=1
                    print('第%s个子线程开始执行：'%i)
                    chirldProcess(key, baiduSearch)
                    print('第%s个子线程执行完毕'%i)
            t = threading.Thread(target=loop, name='LoopThread',args=(i,))
            t.start()
            t.join()
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static/stockAnalysis/json/baidu.json'), 'w', encoding='utf-8')as f:
                json.dump(baiduSearch, f, ensure_ascii=False)
            '''
            end = time.time()
            print('\n-----------------------\n任务一共执行了 %0.2f seconds.\n' %
                  ((end - start)))

        except:
            traceback.print_exc()
    elif a == 'a':
        # 首先读取数据：
        with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static/stockAnalysis/json/baidu.json'), 'r', encoding='utf-8')as f:
            textDict = json.load(f)
        textFreq = {}
        backgroudImagePath = os.path.join(os.path.join(os.path.dirname(
            os.path.dirname(__file__))), 'static/stockAnalysis/img/back.png')
        backgroudImage = plt.imread(backgroudImagePath)

        def loop1(textDict):
            for i in textDict:
                textFreq[i] = int(textDict[i]['num'])
        t = threading.Thread(target=loop1, name='LoopThread', args=(textDict,))
        t.start()
        t.join()
        j = 0
        for i in textDict:
            j += 1
            news = ''
            for k in textDict[i]['news']:
                news += '\n    '+k['news']+'\n'+'    '+k['url']
            with open(os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__))), 'static/stockAnalysis/json/baiduAnalysis.txt'), 'a', encoding='utf-8') as f:
                f.write('第%s支热点股票<%s>：\n  新闻频次：%s\n  新闻：%s\n' %
                        (j,i,textDict[i]['num'], news))
        '''设置词云样式'''
        wc = WordCloud(
            background_color='white',  # 设置背景颜色
            mask=backgroudImage,  # 设置背景图片
            font_path='C:\Windows\Fonts\STZHONGS.TTF',  # 若是有中文的话，这句代码必须添加，不然会出现方框，不出现汉字
            max_words=2000,  # 设置最大现实的字数
            stopwords=STOPWORDS,  # 设置停用词
            max_font_size=80,  # 设置字体最大值
            random_state=100  # 设置有多少种随机生成状态，即有多少种配色方案
        )
        with open(os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__))), 'static/stockAnalysis/json/baiduAnalysis.json'), 'w', encoding='utf-8') as f:
            json.dump(textFreq, f, ensure_ascii=False)
        # 加载文本
        wc.generate_from_frequencies(textFreq)
        print('开始加载文本')
        # 改变字体颜色
        img_colors = ImageColorGenerator(backgroudImage)
        # 字体颜色为背景图片的颜色
        wc.recolor(color_func=img_colors)
        # 显示词云图
        plt.imshow(wc)
        # 是否显示x轴、y轴下标
        plt.axis('off')
        # plt.show()
        # os.path.join()：  将多个路径组合后返回
        wc.to_file(os.path.join(os.path.join(os.path.dirname(
            os.path.dirname(__file__))), 'static/stockAnalysis/img/baiduAnalysis.jpg'))
        print('生成词云成功!')

    else:
        print('感谢使用')
    print('%0.2f' % time.time())
