#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 笔趣阁爬虫 '

__author__ = 'fslong'

import requests
import re
import pyquery


def bookSearch(key):
    url = 'http://www.biquge.com.tw/modules/article/soshu.php'
    data = {'searchkey': key}
    userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17704'
    headers = {'User-Agent': userAgent, }
    req = requests.post(url, data=data, headers=headers,timeout=8)
    return(req.text)


if __name__ == '__main__':
    print(bookSearch('圣墟'))
