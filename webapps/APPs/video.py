#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import pyquery
import json


def getVideo(videoUrl):

    referer = 'https://api.daidaitv.com/index/?url='+videoUrl
    # 另外的接口：jx.598110.com/index.php?url=
    '''
    {url: "http://goudidiao.com/?url=", title: "综合线路④"},
    {url: "http://api.baiyug.cn/vip/index.php?url=", title: "综合线路⑤"},
    {url: "http://www.sonimei.cn/?url=", title: "综合线路⑥"},
    {url: "https://api.vparse.org/?url=", title: "腾讯接口①"},
    {url: "https://jx.maoyun.tv/index.php?id=", title: "腾讯接口②"},
    {url: "http://pupudy.com/play?make=url&id=", title: "综合线路⑦"},
    {url: "http://www.qxyingyuan.vip/play?make=url&id=", title: "优酷接口①"},
    {url: "http://appapi.svipv.kuuhui.com/svipjx/liulanqichajian/browserplugin/qhjx/qhjx.php?id=", title: "综合线路"},
    {url: "http://api.xfsub.com/index.php?url=", title: "1905优先接口"},
    {url: "https://jiexi.071811.cc/jx.php?url=", title: "综合线路⑧"},
    {url: "http://www.sfsft.com/admin.php?url=", title: "综合线路⑨"},
    {url: "http://q.z.vip.totv.72du.com/?url=", title: "综合线路⑩"},
    {url: "http://aikan-tv.com/?url=", title: "综合线路⑪(不太稳定)"},
    {url: "http://jx.api.163ren.com/vod.php?url=", title: "腾讯接口①"},
    {url: "http://www.wmxz.wang/video.php?url=", title: "综合线路⑫"},
    {url: "http://v.renrenfabu.com/jiexi.php?url=", title: "综合线路⑬"},
    {url: "http://jx.598110.com/zuida.php?url=", title: "综合线路③"},
    {url: "http://jx.598110.com/duo/index.php?url=", title: "综合线路②"},
    {url: "http://jx.598110.com/index.php?url=", title: "综合线路①"}
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
