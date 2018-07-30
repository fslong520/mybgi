import json
import os
import re
import threading
import traceback

import jieba
import pyquery
import requests
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.


class Stock(object):
    def __init__(self):
        self.path = os.path.dirname(__file__)
        self.userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17704'
        self.headers = {'User-Agent': self.userAgent, }
        self.url = {'weibo': 'https://d.weibo.com/230771',  # 微博股票频道
                    'toutiaoUrl': 'https://www.toutiao.com/api/pc/feed/?category=stock&utm_source=toutiao&widen=1&max_behot_time=1532523143&max_behot_time_tmp=1532523143&tadrequire=true&as=A1757BA5D9F15B9&cp=5B59B1559B695E1&_signature=NtaxXQAAbZaeXPnEGZpa0TbWsU',  # 今日头条股票频道
                    'stocklist': 'http://quote.eastmoney.com/stocklist.html',  # 东方财富网股票代码列表
                    'xueqiu': 'https://xueqiu.com/v4/statuses/public_timeline_by_category.json',  # 雪球各专栏
                    'stockvalue': 'https://stock.xueqiu.com/v5/stock/realtime/quotec.json', # 雪球股票指数
                    'xueqiunews': 'https://xueqiu.com/statuses/hots.json',# 雪球新闻
                    }

    def weiboStock(self):
        path = self.path
        print('当前文件所在文件夹：%s' % path)
        cookies = {'Cookie': 'login_sid_t=39d73e11482817bc85e3c441df5cd59b; cross_origin_proto=SSL; _s_tentry=-; Apache=4641919282416.988.1532569713780; UOR=,,www.jijidown.com; SINAGLOBAL=4743551653952.5625.1525937284248; ALF=1564105865; SCF=Aszz_unMZy149N0itsldsDVLmecrGtJIU-LomtUrpjDgLx9LYXammBVQbU9pVNwoI-6Z9zRGDzvRiMH-ZVg7fn0.; ULV=1532569713811:31:7:2:4641919282416.988.1532569713780:1532488658134; SUHB=0gHUi7TXrXOuK9; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh5vzMP3YnB8Uzr47E95MNf5JpX5K2hUgL.Fo27ehnXShzXS0e2dJLoIEXLxK-L1h-LB-eLxK-LB-BL1K5LxKML1h-LBKMLxKqL1KnL12-LxKML1hML1hnt; SUB=_2A252XVleDeRhGedO61oV9CzIzD-IHXVVK82WrDV8PUNbmtBeLUTEkW9NIfGZgFD3mdt1t2kXkAcAOgy_ubzhF3e3; SSOLoginState=1532569870; wvr=6'}
        #url = self.url['weibo']
        stockAll = []

        def pageInpage(n, m):
            newUrl = 'https://d.weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=230771&current_page='+str(n)+'&since_id=&page='+str(
                m)+'&pagebar=0&tab=home&pl_name=Pl_Core_MixedFeed__5&id=230771&script_uri=/230771&feed_type=1&pre_page=2&domain_op=230771&__rnd=1532589380570'
            req = requests.get(newUrl, headers=self.headers,
                               cookies=cookies, timeout=20).text
            req=json.loads(req)
            stocks = re.findall(r'\$.*?\s.{2}\d{6}\$',req['data'])
            print('第%s页的第%s小页：%s' % (m,n%3+1, stocks))
            stockAll[0:0] = stocks

        # 新线程执行的代码:
        def loop():
            print('thread %s is running...' % threading.current_thread().name)
            n = 0
            while n < 7:            
                try:
                    if n==0:
                        pageInpage(3, n+1)
                        pageInpage(1, n+1)                        
                        print('第一页比较特殊')
                    else:
                        pageInpage(3*n, n+1)
                        pageInpage(3*n+1, n+1)
                        pageInpage(3*n+2, n+1)
                except:
                    traceback.print_exc()
                n = n + 1
                print('thread %s >>> %s' %
                      (threading.current_thread().name, n))
            print('thread %s ended.' % threading.current_thread().name)

        print('thread %s is running...' % threading.current_thread().name)
        t = threading.Thread(target=loop, name='LoopThread')
        t.start()
        t.join()
        print('thread %s ended.' % threading.current_thread().name)

        print('总的股票列表：%s' % stockAll)
        tj = {}
        for i in stockAll:
            if i in tj:
                tj[i] += 1
            else:
                tj[i] = 1
        for i in tj:
            print('\n%s:%s' % (i, tj[i]))
        return tj

    def getStockList(self):
        if os.path.isfile(os.path.join(self.path, 'static/stockAnalysis/json/stocklistTest.json')):
            with open(os.path.join(self.path, 'static/stockAnalysis/json/stocklistTest.json'), 'r', encoding='utf-8') as f:
                stocklistDict = json.load(f)
        else:
            try:
                url = self.url['stocklist']
                req = requests.get(url, headers=self.headers,
                                   timeout=20).content.decode('gbk')
                PQreq = pyquery.PyQuery(req)
                stocklistDict = {'sh': [], 'sz': []}
                stocklistDictUl = PQreq('#quotesearch > ul').items()
                k = True
                for i in stocklistDictUl:
                    for j in i('li > a').items():
                        if j.attr.name == '':
                            pass
                        else:
                            stockString = j.text()
                            # print(stockString)
                            if k:
                                stocklistDict['sh'].append((stockString.split(
                                    '(')[0], 'SH'+stockString.split('(')[1][0:-1]))
                            else:
                                stocklistDict['sz'].append((stockString.split(
                                    '(')[0], 'SZ'+stockString.split('(')[1][0:-1]))
                    k = False
                with open(os.path.join(self.path, 'static/stockAnalysis/json/stocklist.json'), 'w', encoding='utf-8') as f:
                    json.dump(stocklistDict, f, ensure_ascii=False)

            except:
                traceback.print_exc()
            finally:
                return stocklistDict

    def xueqiuAnalysis(self):  # 雪球的反爬虫真屌，搞不定
        def xueqiuZhuanlan(self):
            for category in (-1, 6, 105, 111, 104, 113, 110):
                params = {'since_id': -1,
                          'max_id': -1, 'count': 15, 'category': category}
                # 其中category控制栏目，-1：头条，6：直播，105：沪深，111：房产，102：港股，104：基金，101：美股，113：私募，110：保险
                # since_id和max_id顾名思义，控制的是资讯的起始位置与结束位置，count控制的是获取资讯的条目数
                cookies = {'Cookie': 'xq_a_token=aef774c17d4993658170397fcd0faedde488bd20; xq_a_token.sig=F7BSXzJfXY0HFj9lqXif9IuyZhw; xq_r_token=d694856665e58d9a55450ab404f5a0144c4c978e; xq_r_token.sig=Ozg4Sbvgl2PbngzIgexouOmvqt0; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1532583834; bid=c73b27a724221ffb1601c2f9283f3429_jizm5ddk; device_id=92a668d144fc509b73d74d28ef0d8c31; s=fm11nkb0c6; u=931532573730800; _ga=GA1.2.406271030.1526360070; Hm_lvt_1db88642e346389874251b5a1eded6e3=1530253972,1530255153,1531202643,1532573733'}
                url = self.url['xueqiu']
                req = requests.get(
                    url, params=params, headers=self.headers, cookies=cookies, timeout=20).text
                print(req)

        def xueqiuNews(self):
            params = {'a': 1, 'count': 10, 'page': 1,
                      'meigu': 0, 'scope': 'day', 'type': 'news'}
            url = self.url['xueqiu']
            req = requests.post(
                url, data=params, headers=self.headers, timeout=20).text
            print(req)
            return(req)
        return(xueqiuNews(self))

    def stockvalue(self,key):
        params = {'symbol': key}
        url = self.url['stockvalue']
        req = requests.get(url, headers=self.headers,params=params,timeout=20).text
        stockValue=json.loads(req)
        return stockValue



if __name__ == '__main__':

    stock = Stock()
    for i in stock.weiboStock():
        key = i.split(' ')[1][0:-1].upper()
        print(stock.stockvalue(key))
    '''
    with open(os.path.join(os.path.dirname(__file__),'static/stockAnalysis/json/weibo.json'),'r',encoding='utf-8') as f:
        print(json.load(f))
    '''
