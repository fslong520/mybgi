from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render

from webapps.APPs import bingPic, weather, video

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


def getVideo(request):
    url = request.GET.get('url', 0)
    videoUrl = video.getVideo(url)
    if videoUrl != False:
        return HttpResponse(videoUrl)
    else:
        return HttpResponse(False)
