#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 笔趣读爬虫 '

__author__ = 'fslong'

import requests
import re
import pyquery


def bookSearch(key):
    url = 'https://www.biqudu.com/searchbook.php'
    data = {'keyword': key}
    userAgent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'
    headers = {'User-Agent': userAgent, 'Connection': 'close', }
    requests.adapters.DEFAULT_RETRIES = 5
    req = requests.get(url, params=data, headers=headers,timeout=8)
    PQreq = pyquery.PyQuery(req.text)
    bookInfo = []
    for i in PQreq('#item').items():
        bookName = i('dl dt a').text()
        author = i('dl dt span').text()
        intro = i('dl dd').text()
        bookInfo.append(
            {'bookName': bookName, 'author': author, 'intro': intro, })
    return(bookInfo)


if __name__ == '__main__':
    print(bookSearch('太上章'))
