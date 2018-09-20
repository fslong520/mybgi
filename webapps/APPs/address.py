#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 根据ip获取地址模块 '

__author__ = 'fslong'

import json
import re

import pyquery
import requests


def getAdressByIP(ip='112.103.201.146'):
    url = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?query='+ip+'&resource_id=6006&format=json'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17692'}
    data = {}
    req = requests.get(url, data=data, headers=headers, timeout=8).text
    req = re.match(r'(.*\()(.*)(\)\;)', req)
    reqDict = json.loads(req.group(2))
    cityName = reqDict['data'][0]['location'].split(' ')[0]
    cityName1 = re.match(r'(.*)(省)(.*)', cityName[0:-1])
    cityName2 = re.match(r'(.*)(自治区)(.*)', cityName[0:-1])
    cityName3 = re.match(r'(.*)(市)(.*)', cityName[0:-1])
    if cityName1:
        cityName = cityName1.group(3)
        # print(cityName+'\n')
    elif cityName2:
        cityName = cityName2.group(3)
        # print(cityName+'\n')
    elif cityName3:
        cityName = cityName3.group(3)
        # print(cityName+'\n')

    return(cityName)


if __name__ == '__main__':
    print(getAdressByIP())
