import json

from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render

from apis.apiApps import todayWallpaper
from spiders.book import kgbook
from webapps.APPs import bingPic
from webapps.APPs import getWeather as weather


# Create your views here.
def getBingPic(request):
    idx = request.GET.get('idx', 0)
    picDict = bingPic.getBingPicUrl(idx, 1)
    return JsonResponse(picDict)


def getWeather(request):
    cityName = request.GET.get('cityname', '')
    weatherList = weather.getWether(cityName=cityName)
    return JsonResponse(weatherList)


def test(request):
    return render(request, 'apis/testApis.html')


def searchBooks(request):
    bookName = request.GET.get('bookName')
    if bookName == '':
        return HttpResponse('好像没输入要查询的电子书的名称呀！')
    else:
        return JsonResponse(kgbook.searchBooks(bookName))


def getTodayWallpaper(request):
    try:
        picType = int(request.GET.get('picType', 0))
        num = int(request.GET.get('num', 1))
        transfer = int(request.GET.get('transfer', 0))
    except:
        picType = 0
        num = 1
        transfer = 0
    try:
        picsList = todayWallpaper.wallpaper(picType, num, transfer)
    except:
        picsList = []
    if picsList != []:
        success = True
    else:
        success = False
    picsDict = {'success': success, 'picData': picsList}

    return JsonResponse(
        picsDict,
        content_type='application/json;charset=utf-8',
        json_dumps_params={'ensure_ascii': False})
