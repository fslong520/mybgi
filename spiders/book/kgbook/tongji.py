#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 苦瓜书城爬虫数据统计 '

__author__ = 'fslong'

import os
import re


def readBookColumnData():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'columndata.txt'), 'r', encoding='utf-8') as f:
        columns = []
        for line in f.readlines():
            column = re.match(r'^(.*)(栏目一共)(.*)(本书)$', line.strip()).groups()
            columns.append([column[0], int(column[2])])
        bookNumMax = 0
        allBooks=0
        for column in columns:
            if column[1] > bookNumMax:
                bookNumMax = column[1]
            allBooks+=column[1]
        for column in columns:
            column.append(column[1]*100/bookNumMax)
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'columndata.html'), 'a', encoding='utf-8') as f1:
                html = '<tr><td style="width: 100px"><strong>%s：</strong></td><td><progress class="uk-progress" value="%s" max="100" style="margin-top: 5px"></progress></td><td style="width: 150px">合计%s本书。</td></tr>' % (
                    column[0], column[2], column[1])
                f1.write(html)
            print(column)
        print('小说本数最大值'+str(bookNumMax))
        print(allBooks)


if __name__ == '__main__':
    readBookColumnData()
