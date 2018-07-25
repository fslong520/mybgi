#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 词云玩玩 '

__author__ = 'fslong'
import os
import json
path = os.path.dirname(__file__)
with open(os.path.join(path, 'kgbook.json'), 'r', encoding='utf-8') as f:
    books = json.load(f)
    wordStr = ''
    for book in books:
        wordStr += book['bookName']+book['intro']
    print(wordStr)
