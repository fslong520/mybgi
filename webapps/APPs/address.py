#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import pyquery
import json


def getAdressByIP(ip='47.106.197.182'):
    url = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?query='+ip+'&co=&resource_id=6006&t=1529930205766&ie=utf8&oe=gbk&cb=op_aladdin_callback&format=json&tn=baidu&cb=jQuery110208006588187590413_1529929325310&_=1529929325336'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17692'}
    data = {}
    req = requests.get(url,data=data,headers=headers,timeout=8).text
    return(req)
    
print(getAdressByIP())

