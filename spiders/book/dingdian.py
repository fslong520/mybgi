#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 顶点小说 '

__author__ = 'fslong'

import requests
import re
import pyquery


class Book(object):
    def __init__(self):
        self.bookName = ''

    def bookSearch(self, keyword):
        url = 'https://www.dingdiann.com/searchbook.php'
        data = {'keyword': keyword}
        userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17704'
        headers = {'User-Agent': userAgent, 'Connection': 'close', }
        req = requests.post(url, data=data, headers=headers, timeout=8)
        PQreq = pyquery.PyQuery(req.text)('.novelslist2 ul li').items()
        print(req.text)
        for i in PQreq:
            print(i)
            if i.text() == '':
                print(req.text)
            if i('.s1').text() == '作品分类':
                print(i.text())
            else:
                print(i.text())
                self.bookName = i('.s1').text()


if __name__ == '__main__':
    book = Book()
    book.bookSearch('太上章')
    print(book.bookName)
