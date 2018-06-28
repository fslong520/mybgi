#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import pyquery
import json


class Port(object):
    def __init__(self):
        self.ports = [
            {'id': 'port0',
                'url': "https://api.daidaitv.com/index/?url=",
                'title': "综合线路"
             }, {
                'id': 'port1',
                'url': "http://xlyy100.com/xlyy.php?url=",
                'title': "综合线路1"
            }, {
                'id': 'port2',
                'url': "http://api.baiyug.cn/vip/index.php?url=",
                'title': "综合线路2"
            }, {
                'id': 'port3',
                'url': "http://www.sonimei.cn/?url=",
                'title': "综合线路3"
            }, {
                'id': 'port4',
                'url': "https://api.varse.org/?url=",
                'title': "腾讯接口1"
            }, {
                'id': 'port5',
                'url': "https://jx.maoyun.tv/index.php?id=",
                'title': "腾讯接口2"
            }, {
                'id': 'port6',
                'url': "http://pupudy.com/play?make=url&id=",
                'title': "综合线路4"
            }, {
                'id': 'port7',
                'url': "http://www.qxyingyuan.vip/play?make=url&id=",
                'title': "优酷接口1"
            }, {
                'id': 'port8',
                'url': "http://appapi.svipv.kuuhui.com/svipjx/liulanqichajian/browserplugin/qhjx/qhjx.php?id=",
                'title': "综合线路5"
            }, {
                'id': 'port9',
                'url': "http://api.xfsub.com/index.php?url=",
                'title': "1905优先接口"
            }, {
                'id': 'port10',
                'url': "https://jiexi.071811.cc/jx.php?url=",
                'title': "综合线路6"
            }, {
                'id': 'port11',
                'url': "http://www.sfsft.com/admin.php?url=",
                'title': "综合线路7"
            }, {
                'id': 'port12',
                'url': "http://q.z.vip.totv.72du.com/?url=",
                'title': "综合线路8"
            }, {
                'id': 'port13',
                'url': "http://aikan-tv.com/?url=",
                'title': "综合线路9(不太稳定)"
            }, {
                'id': 'port14',
                'url': "http://jx.api.163ren.com/vod.php?url=",
                'title': "腾讯接口3"
            }, {
                'id': 'port15',
                'url': "http://www.wmxz.wang/video.php?url=",
                'title': "综合线路10"
            }, {
                'id': 'port16',
                'url': "http://v.renrenfabu.com/jiexi.php?url=",
                'title': "综合线路11"
            }, {
                'id': 'port17',
                'url': "http://jx.598110.com/zuida.php?url=",
                'title': "综合线路③"
            }, {
                'id': 'port18',
                'url': "http://jx.598110.com/duo/index.php?url=",
                'title': "综合线路12"
            }, {
                'id': 'port19',
                'url': "http://jx.598110.com/index.php?url=",
                'title': "综合线路13"
            }, {
                'id': 'port20',
                'url': "https://jx.biaoge.tv/?url=",
                'title': "综合线路13"
            }, ]


def getVideo(videoUrl, portId):
    ports = Port().ports
    port = ''
    for i in ports:
        if i['id'] == portId:
            port = i['url']
            break

    referer = port+videoUrl
    '''

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
