from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render

import pickle
from .APPs import address, bingPic, getWeather, video,transformStr

# Create your views here.


def index(request):
    ports = video.Port().ports
    if request.META.get('HTTP_X_FORWARDED_FOR', '') != '':
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META.get('REMOTE_ADDR', '')
    if ip == '127.0.0.1' or ip == None or ip == '':
        cityName = ''
    else:
        cityName = address.getAdressByIP(ip=ip)
    picDict = bingPic.getBingPicUrl()
    weatherStr = str(getWeather.getWttr(cityName=cityName))
    context = {'picDict': picDict, 'weatherStr': weatherStr, 'ports': ports, }
    return render(request, 'webapps/index.html', context=context)


def getBingPicUrl(request):
    idx = request.GET.get('idx', 0)
    picDict = bingPic.getBingPicUrl(idx, 1)
    return JsonResponse(picDict)


def getVideo(request):
    url = request.GET.get('url', '')
    portId = request.GET.get('port', 'port1')
    videoUrl = video.getVideo(url, portId)
    if videoUrl != False:
        return HttpResponse(videoUrl)
    else:
        return HttpResponse(False)


def getString(request):
    string = request.POST.get('string', '')
    stringMethod = request.POST.get('method', '')
    result=transformStr.transformStr(string,stringMethod)
    if result==False:
        return HttpResponse('抱歉，转换失败！')
    else:
        return HttpResponse(result)
    
