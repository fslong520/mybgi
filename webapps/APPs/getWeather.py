#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 天气模块 '

__author__ = 'fslong'

import json
import pickle
import re

import pyquery
import requests


def getCity(cityName):
    url = 'http://toy1.weather.com.cn/search'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17692'}
    params = {'cityname': cityName, }
    cityRef = requests.get(url=url, params=params, headers=headers)
    cityContent = cityRef.text
    cityJson = cityContent[1:-1]
    cityDict = json.loads(cityJson)
    cityList = []
    for i in cityDict:
        cityList.append(i['ref'].split('~'))
    return cityList


def str2json(weather):
    weather = weather.strip()
    weather = re.sub('\n', '', weather)
    weather = re.sub('\r', '', weather)
    weather = re.sub('\t', '', weather)
    weather = re.sub(' ', '', weather)
    weather = re.sub('&#13;', '', weather)
    weather = re.sub('<script>', '', weather)
    weather = re.sub('</script>', '', weather)
    weather = re.sub('var', '', weather)
    weather = re.sub('hour3data=', '{"hour3data":', weather)
    weather = re.sub('uptime=', '"uptime":', weather)
    weather = re.sub('eventDay=', '"eventDay":', weather)
    weather = re.sub('eventNight=', '"eventNight":', weather)
    weather = re.sub('fifDay=', '"fifDay":', weather)
    weather = re.sub('fifNight=', '"fifNight":', weather)
    weather = re.sub('sunup=', '"sunup":', weather)
    weather = re.sub('sunset=', '"sunset":', weather)
    weather = re.sub('blue=', '"blue":', weather)
    weather = re.sub('hour3week=', '"hour3week":', weather)
    weather = re.sub(';', ',', weather)
    weather = weather[0:-1] + '}'
    return weather


def getWether(cityName='北京'):
    cityList = getCity(cityName)
    '''
    print('查找到的城市有：')
    for i in range(len(cityList)):
        print('%s:%s' % (i+1, cityList[i][2]))
    if len(cityList) > 1:
        a = input('\n请输入要查询城市的序号：')
        try:
            a = int(a)
            city = cityList[a-1]
        except:
            print('输入错误，请重试！')
            return False
    else:
        city = cityList[0]
    '''
    weatherDictAllCity = {}
    for city in cityList:
        cityId = city[0]
        url = 'http://www.weather.com.cn/weather1dn/'+cityId+'.shtml'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17692'}
        try:
            cityWeatherPage = requests.get(
                url=url, headers=headers, timeout=8).text
            cityWeatherPagePyQuery = pyquery.PyQuery(cityWeatherPage)
            weather = str(cityWeatherPagePyQuery('.todayRight script'))
            weather = str2json(weather)
            weather = json.loads(weather)
            windDY = ['无持续风向', '东北风', '东风', '东南风',
                      '南风', '西南风', '西风', '西北风', '北风', '旋转风']
            windJB = ['<3级', '3-4级', '4-5级', '5-6级', '6-7级',
                      '7-8级', '8-9级', '9-10级', '10-11级', '11-12级']
            qxbm = {'0': '晴',
                    '1': '多云',
                    '2': '阴',
                    '3': '阵雨',
                    '4': '雷阵雨',
                    '5': '雷阵雨伴有冰雹',
                    '6': '雨夹雪',
                    '7': '小雨',
                    '8': '中雨',
                    '9': '大雨',
                    '10': '暴雨',
                    '11': '大暴雨',
                    '12': '特大暴雨',
                    '13': '阵雪',
                    '14': '小雪',
                    '15': '中雪',
                    '16': '大雪',
                    '17': '暴雪',
                    '18': '雾',
                    '19': '冻雨',
                    '20': '沙尘暴',
                    '21': '小到中雨',
                    '22': '中到大雨',
                    '23': '大到暴雨',
                    '24': '暴雨到大暴雨',
                    '25': '大暴雨到特大暴雨',
                    '26': '小到中雪',
                    '27': '中到大雪',
                    '28': '大到暴雪',
                    '29': '浮尘',
                    '30': '扬沙',
                    '31': '强沙尘暴',
                    '53': '霾',
                    '99': '无',
                    '32': '浓雾',
                    '49': '强浓雾',
                    '54': '中度霾',
                    '55': '重度霾',
                    '56': '严重霾',
                    '57': '大雾',
                    '58': '特强浓雾',
                    '97': '雨',
                    '98': '雪',
                    '301': '雨',
                    '302': '雪'
                    }
            #print('%s未来7日天气情况：\n' % city[2])
            weatherList = []
            for i in weather['hour3data']:
                for j in i:
                    # return ('时间：%s，温度：%s℃ ，湿度%s%%，%s，风力%s风向%s' % (j['jf'][0:4]+'年'+j['jf'][4:6]+'月'+j['jf'][6:8]+'日'+j['jf'][8:10]+'时', j['jb'], j['je'], qxbm[str(
                    # int(j['ja']))], windJB[int(j['jc'])], windDY[int(j['jd'])]))
                    time = j['jf'][0:4]+'年'+j['jf'][4:6] + \
                        '月'+j['jf'][6:8]+'日'+j['jf'][8:10]+'时'
                    temperature = j['jb']
                    humanity = j['je']
                    wind = '风力'+windJB[int(j['jc'])]+'，风向'+windDY[int(j['jd'])]
                    weatherInfo = qxbm[str(int(j['ja']))]
                    weatherDict = {'time': time, 'temperature': temperature,
                                   'humanity': humanity, 'wind': wind, 'weatherInfo': weatherInfo, }
                    weatherList.append(weatherDict)
            weatherDictAllCity[city[5]] = {
                'weatherList': weatherList, 'city': city, }
        except:
            weatherDictAllCity[city[5]] = '抱歉，暂时未收录%s的天气数据。' % city[2]
    return weatherDictAllCity


# getWether(input('\n请输入要查询天气的城市名称或区号或邮编或简称或拼音全拼：'))

def getWttr(cityName=''):
    if cityName == '':
        city = ''
        url = 'http://wttr.in/'
    else:
        cityList = getCity(cityName)
        '''
        for i in range(len(cityList)):
            print('%s:%s' % (i+1, cityList[i][2]))
        if len(cityList) > 1:
            a = input('\n请输入要查询城市的序号：')
            try:
                a = int(a)
                city = cityList[a-1]
            except:
                print('输入错误，请重试！')
                return False
        else:
            city = cityList[0]
        '''
        city=cityList[0]
        url = 'http://wttr.in/'+city[5]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17692'}
    params = {'lang': 'zh'}
    try:
        cityWeatherPage = requests.get(
            url, params=params, headers=headers, timeout=8).text
        cityWeatherPagePyQuery = pyquery.PyQuery(cityWeatherPage)
        return cityWeatherPagePyQuery('pre')
    except:
        return '查询失败。'

if __name__=='__main__':
    print(getCity(input('cityname:')))
