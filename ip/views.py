from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from ip.models import IP
import pickle
# Create your views here.


def index(request):
    if request.META.get('HTTP_X_FORWARDED_FOR', '') != '':
        nowIp = request.META['HTTP_X_FORWARDED_FOR']
    else:
        nowIp = request.META.get('REMOTE_ADDR', '')
    name='匿名'    
    try:
        ip = IP.objects.get(name=name)
    except:
        ip=IP()
    ip.name = name
    ip.ip=nowIp
    allIp=IP.objects.all()
    context = {'ip': ip, 'name': nowIp,'allIp':allIp}
    ip.save()
    return render(request, 'ip/index.html', context=context)
    
# 存储IP地址：


def saveIp(request,name):
    if request.META.get('HTTP_X_FORWARDED_FOR', '') != '':
        nowIp = request.META['HTTP_X_FORWARDED_FOR']
    else:
        nowIp = request.META.get('REMOTE_ADDR', '')
    try:
        ip = IP.objects.get(name=name)
    except:
        ip=IP()
    ip.name = name
    ip.ip=nowIp
    allIp=IP.objects.all()
    context = {'ip': ip, 'name': nowIp,'allIp':allIp}
    ip.save()
    return render(request, 'ip/index.html', context=context)
