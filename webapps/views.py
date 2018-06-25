from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render

from webapps.APPs import bingPic, weather

# Create your views here.


def index(request):
    picDict = bingPic.getBingPicUrl()
    weatherStr = str(weather.getWttr())
    context = {'picDict': picDict, 'weatherStr': weatherStr, }
    return render(request, 'webapps/index.html', context=context)


def getBingPicUrl(request):
    idx = request.GET.get('idx', 0)
    picDict = bingPic.getBingPicUrl(idx, 1)
    return JsonResponse(picDict)
