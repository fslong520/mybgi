from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render

from webapps.APPs import bingPic, weather


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
