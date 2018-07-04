#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 雪球爬虫 '

__author__ = 'fslong'
import json
import pickle
import re

import pyquery
import requests
import random
import time

cookies = 'HMVT=6bcd52f51e9b3dce32bec4a3997715ac|1530256511|; HMACCOUNT=EEA86467782DF08F; BDRCVFR[SL8xzxBXZJn]=mk3SLVN4HKm; PSINO=2; H_PS_PSSID=; BAIDUID=6E1A0F5F897FF29C1B26BC86F5363786:FG=1; BIDUPSID=79C7A5EE0EC2060E7C76882EB70E00F0; PSTM=1525936371; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; MCITY=-160%3A131%3A356%3A48%3A; BDUSS=lFZYzRBeERzUWVKbGlObFB5SXlnM2hoVFlYbVBYMURRVEVKNX5OWmREZ1dFVjFiQVFBQUFBJCQAAAAAAAAAAAEAAABmZwwOZnNsNDcwNjU3NTcwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABaENVsWhDVbU'
url = 'https://xueqiu.com/people'
userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17704'
headers = {'User-Agent': userAgent, 'cookies': cookies}
req = requests.get(url, headers=headers)
reqPQ = pyquery.PyQuery(req.text)
peoples = reqPQ('.info .name').items()
for people in peoples:
    url = 'https://xueqiu.com%s'%people.attr('href')
    reqPeople=requests.get(url, headers=headers)
    reqPeoplePQ=pyquery.PyQuery(reqPeople.text)
    print(people('img').attr('title'))
    print('个人简介：%s'%reqPeoplePQ('.profiles__hd__info p').text())
    time.sleep(30*random.random())
