#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 分析解析获取到的数据 '

__author__ = 'fslong'

import os
import json

path = os.path.dirname(__file__)

with open(os.path.join(path, 'wallpapersite.json'), 'r', encoding='utf-8') as f:
    allData = json.load(f)
columns = {}
for i in allData:
    for j in allData[i]['data']:
        ##print(j)
        column = allData[i]['data'][j]['picColumn']
        try:
            columns[column].append(allData[i]['data'][j]['picUrl'][0]['url'])
        except:
            columns[column] = [allData[i]['data'][j]['picUrl'][0]['url']]
for i in columns:
    with open(os.path.join(path, 'urlsHtml/%s.html'%i), 'w', encoding='utf-8') as f:
        strUrl='<!DOCTYPE html><html><head><meta charset="utf-8" /><meta http-equiv="X-UA-Compatible" content="IE=edge"><title>'+i+'</title><meta name="viewport" content="width=device-width, initial-scale=1"></head><body><p>右键此处网页另存为，选择所有文件即可将本页面图片全部下载！</p>'
        for i in columns[i]:
            strUrl+= '<img src="'+i+'" style="width: 100%"></img>\n'
        f.write(strUrl+'</body></html>')
