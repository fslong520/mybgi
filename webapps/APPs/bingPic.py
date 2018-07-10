#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import pyquery
import json


def getBingPicUrl(idx=0, n=1):
    url = 'https://cn.bing.com/HPImageArchive.aspx'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17692'}
    params = {'idx': idx, 'n': n, 'format': 'js'}
    req = requests.get(url,  params=params, headers=headers, timeout=8)
    print(req.text)
    js = json.loads(req.content.decode('utf-8'))
    return({'date': js['images'][0]['enddate'], 'copyright': js['images'][0]['copyright'], 'url': 'https://cn.bing.com'+js['images'][0]['url']})


# print(getBingPicUrl())
