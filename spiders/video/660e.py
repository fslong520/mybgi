#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 660e '

__author__ = 'fslong'

import requests
import re
import time
import json
import pyquery
import xml
from urllib.request import urlopen, urlretrieve
from xml.parsers.expat import ParserCreate


def getVideoXml(videourl):
    url = 'http://660e.com/api.php'
    data = {'url': videourl,
            'type': '', 'xml': '1', 'key': 'a3579b6a4e6d13b185c6bb85ebcad42e',
            'time': '1530797299'}
    userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17704'
    headers = {'User-Agent': userAgent, }
    page = requests.post(url, data=data, headers=headers)
    pageJson = json.loads(page.text)
    videUrl = 'http://660e.com'+pageJson['url']
    xmlData = requests.get(videUrl, headers=headers).text
    return(xmlData)


class GetVideoByXml(object):
    def __init__(self):  # 因为需要返回解析得数据，所以必须有这一个
        self.video = {
            'video': [],
        }

    def start_element(self, name, attrs):
        self.name = name

    def char_element(self, text):
        if self.name == 'file':
            self.video['video'].append(text)

    def end_element(self, name):
        pass
        #print('sax:end_element: %s' % name)


def videoXml(xml_str):
    handler = GetVideoByXml()
    parser = ParserCreate()
    parser.StartElementHandler = handler.start_element
    parser.CharacterDataHandler = handler.char_element
    parser.EndElementHandler = handler.end_element
    parser.Parse(xml_str)
    return handler.video


result = videoXml(getVideoXml(input('请输入要解析的视频地址：')))
with open('video.txt', 'a', encoding='utf-8') as f:
    for i in result['video']:
        f.write(i+'\n')
    print('视频下载网址获取完毕！')
input()
