#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 苦瓜书城爬虫 '

__author__ = 'fslong'
import json
import pickle
import re

import pyquery
import requests
import random
import time

import os
import sqlite3
# 引入pydbclib，这个模块用于将各种数据库的操作进行统一，不同的数据库改变drive就行
#from pydbclib import connection


def searchBooks(bookName):
    cookies = 'Hm_lpvt_5e28552272120b0ca6ddfed1735fe0d7=1530412264; Hm_lvt_5e28552272120b0ca6ddfed1735fe0d7=1530410512; ecmslastsearchtime=1530412311; ecmsmlusername=fsl470657570; ecmsmluserid=8708; ecmsmlgroupid=1; ecmsmlrnd=9mrsfNXWStMu9wmWzqZD; ecmsmlauth=7affd8a85f625fe46048b2894f132a64'
    url = 'https://kgbook.com/e/search/index.php'
    data = {
        'keyboard': bookName,
        'show': 'title,booksay,bookwriter',
        'tbname': 'download',
        'tempid': '1',
    }
    userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17704'
    headers = {'User-Agent': userAgent, 'cookies': cookies}
    result = requests.post(url, data=data, headers=headers)
    pQResult = pyquery.PyQuery(result.text)
    bookListsHtml = pQResult('#slist li').items()
    bookDicts = {}
    j = 0
    for i in bookListsHtml:
        bookName=''
        j += 1
        bookName = i('strong').text()
        if bookName=='':
            bookName=i('h1 a').text()
        intro = i('.text').text()
        url = i('.url').text()
        date = i('.t').text()
        bookDicts['book'+str(j)] = {'bookName': bookName,
                                    'intro': intro, 'url': url, 'date': date, }
    bookDicts['len'] = j
    return bookDicts


def bookSpider():

    def getColumn():
        cookies = 'Hm_lpvt_5e28552272120b0ca6ddfed1735fe0d7=1530412264; Hm_lvt_5e28552272120b0ca6ddfed1735fe0d7=1530410512; ecmslastsearchtime=1530412311; ecmsmlusername=fsl470657570; ecmsmluserid=8708; ecmsmlgroupid=1; ecmsmlrnd=9mrsfNXWStMu9wmWzqZD; ecmsmlauth=7affd8a85f625fe46048b2894f132a64'
        url = 'https://kgbook.com/'
        data = {}
        userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17704'
        headers = {'User-Agent': userAgent, 'cookies': cookies}
        result = requests.get(url, data=data, headers=headers)
        pQResult = pyquery.PyQuery(result.content.decode('utf-8'))
        columnsHtml = pQResult('#category .row ul li a').items()
        columns = {}
        j = 0
        for i in columnsHtml:
            j += 1
            name = i.text()
            url = i.attr('href')
            columns['column'+str(j)] = {'name': name,
                                        'url': 'https://kgbook.com'+url, }
        columns['len'] = j
        return columns

    # 获取一个不重复的随机列表：

    def randomList(bookNum):
        listResult = []
        i = 0
        # int()函数只能取整，故int(random.random())是取不到1的
        while i < bookNum:
            j = int(bookNum*random.random())+1
            if j in listResult:
                pass
            else:
                listResult.append(j)
                i += 1
        print('以上一共找到%d本书。' % len(listResult))
        return listResult

    def getBooksByColumnUrl(url):
        # 使用非局部变量（不能使用全局变量，全局变量会报错，可能全局变量需要在最外层声明）
        nonlocal bookDefaultNum
        nonlocal bookDefaultDicts
        cookies = 'Hm_lpvt_5e28552272120b0ca6ddfed1735fe0d7=1530412264; Hm_lvt_5e28552272120b0ca6ddfed1735fe0d7=1530410512; ecmslastsearchtime=1530412311; ecmsmlusername=fsl470657570; ecmsmluserid=8708; ecmsmlgroupid=1; ecmsmlrnd=9mrsfNXWStMu9wmWzqZD; ecmsmlauth=7affd8a85f625fe46048b2894f132a64'
        url = url
        data = {}
        userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17704'
        headers = {'User-Agent': userAgent, 'cookies': cookies}
        try:
            result = requests.get(url, data=data, headers=headers, timeout=8)
            pQResult = pyquery.PyQuery(result.content.decode('utf-8'))
            books = pQResult('.channel-item h3 a').items()
            pagenaviA = pQResult('.pagenavi a').items()
            nextPage = ''
            for k in pagenaviA:
                if k.text() == '下一页':
                    nextPage = k
            for i in books:
                bookDefaultNum += 1
                bookName = i.text()
                bookUrl = i.attr('href')
                if bookUrl.startswith('http'):
                    pass
                else:
                    bookUrl = 'https://kgbook.com'+bookUrl
                if i.attr('title'):
                    print('    第%s本书：《%s》' %
                          (int((bookDefaultNum+1)/2), bookName))
                    bookDefaultDicts['book' + str(int((bookDefaultNum+1)/2))
                                     ] = {'bookName': bookName, 'url': bookUrl, }
            bookDefaultDicts['len'] = int((bookDefaultNum+1)/2)
            time.sleep(30*random.random())
        except:
            pass
        finally:
            if nextPage != '':
                getBooksByColumnUrl(nextPage.attr('href'))
            return bookDefaultDicts

    def getBookContent(bookId, url):
        cookies = 'Hm_lpvt_5e28552272120b0ca6ddfed1735fe0d7=1530412264; Hm_lvt_5e28552272120b0ca6ddfed1735fe0d7=1530410512; ecmslastsearchtime=1530412311; ecmsmlusername=fsl470657570; ecmsmluserid=8708; ecmsmlgroupid=1; ecmsmlrnd=9mrsfNXWStMu9wmWzqZD; ecmsmlauth=7affd8a85f625fe46048b2894f132a64'
        url = url
        data = {}
        userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17704'
        headers = {'User-Agent': userAgent, 'cookies': cookies}
        try:
            result = requests.get(url, data=data, headers=headers, timeout=8)
            pQResult = pyquery.PyQuery(result.content.decode('utf-8'))
            bookName = pQResult('#content h1').text()
            bookImg = pQResult('#news_picture img').attr('src')
            if bookImg.startswith('http'):
                pass
            else:
                bookImg = 'https://kgbook.com'+bookImg
            bookDetailsHtml = pQResult('#news_details li').items()
            bookDetails = {}
            bookDetails['bookId'] = bookId
            bookDetails['bookName'] = bookName
            bookDetails['bookImg'] = bookImg
            for i in bookDetailsHtml:
                sx = i.text().split('：')
                if len(sx) > 1:
                    if sx[1] != '':
                        bookDetails[sx[0]] = sx[1]
            bookDetails['intro'] = pQResult('#introduction p').text()
            downloadUrlHtml = pQResult('#introduction a').items()
            for i in downloadUrlHtml:
                bookDetails[i.text()] = i.attr('href')
            time.sleep(30*random.random())
            return bookDetails
        except:
            return False

    def saveBook2Json(column, dicts):
        if os.path.isfile(column+'.json'):
            with open(column+'.json', 'rb') as f:
                try:
                    bookDicts = json.load(f)
                except:
                    bookDicts = {}
                    bookDicts[column] = {}
        else:
            bookDicts = {}
            bookDicts[column] = {}
        bookDicts[column][dicts['bookId']] = dicts
        with open(column+'.json', 'w', encoding='utf-8') as f:
            json.dump(bookDicts, f, ensure_ascii=False)
    columns = getColumn()
    print(columns)
    a=0
    b=27
    for j in columns:
        bookDefaultNum = 0
        bookDefaultDicts = {}
        print('开始查找“%s”栏目的图书' % columns[j]['name'])
        bookDicts = getBooksByColumnUrl(columns[j]['url'])
        a+=bookDicts['len']
        bookRandomList = randomList(bookDicts['len'])
        with open('columndata.txt', 'a', encoding='utf-8') as f:
            f.write('%s栏目一共%s本书\n'%(columns[j]['name'], bookDicts['len'])) 
        for i in bookRandomList:
            bookId = 'book'+str(i)
            book = getBookContent(bookId, bookDicts[bookId]['url'])
            if book == False:
                bookDicts[bookId]['bookId'] = bookId
                bookDicts[bookId]['badData'] = True
                saveBook2Json(columns[j]['name'], bookDicts[bookId])
                try:
                    print('    《%s》的数据获取完毕!' % bookDicts[bookId]['bookName'])
                except:
                    pass
            else:
                saveBook2Json(columns[j]['name'], book)
                print('    《%s》的数据获取完毕!' % book['bookName'])
        print('----------------------------------------------------')
    print('下载完毕,%s个栏目%s本书')%(b,a)


if __name__ == '__main__':
    bookSpider()
