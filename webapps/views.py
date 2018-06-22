from django.shortcuts import render
from django.http.response import HttpResponse,JsonResponse
from webapps.APPs import bingPic

# Create your views here.


def index(request):
    picDict = bingPic.getBingPicUrl()
    context = {'picDict': picDict}
    return render(request, 'webapps/index.html', context=context)


def getBingPicUrl(request):
    idx = request.GET.get('idx',0)
    picDict = bingPic.getBingPicUrl(idx,1)
    return JsonResponse(picDict)
