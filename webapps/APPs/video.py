#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import pyquery
import json


def getVideo(videoUrl):

    referer = 'http://jiexi.071811.cc/jx.php?url='+videoUrl
    '''
    url = 'http://jiexi.071811.cc/api/xit.php'
    if 'iqiyi' in videoUrl:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17692'}
            data = {'referer': referer,
                    'time': '',
                    'key': 'nfQcEwMjg0LgqPh_ahKDmsvhpJ4=',
                    'url': videoUrl,
                    'type': 'iqiyi',
                    'pc': '0'}
            req = requests.post(url=url, data=data, headers=headers,
                                timeout=8).content.decode('utf-8-sig')
            req = json.loads(req)
            if req['success'] == '1':
                return 'http://jiexi.071811.cc'+req['url']
            else:
                return False
        except:
            return False
    else:
        return referer
    '''
    return referer
