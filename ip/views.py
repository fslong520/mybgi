from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from ip.models import IP
import pickle
# Create your views here.


def index(request):
    if request.META.get('HTTP_X_FORWARDED_FOR', '') != '':
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META.get('REMOTE_ADDR', '')
    name='匿名'
    allIp=IP.objects.all()
    context = {'ip': ip, 'name': name,'allIp':allIp}
    try:
        ip = IP.objects.get(name=name)
    except:
        ip=IP()
    ip.name = name
    ip.ip = ip.save()
    return render(request, 'ip/index.html', context=context)
    
# 存储IP地址：


def saveIp(request,name):
    if request.META.get('HTTP_X_FORWARDED_FOR', '') != '':
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META.get('REMOTE_ADDR', '')
    if ip == '127.0.0.1' or ip == None or ip == '':
        ip = '127.0.0.1'    
    allIp=IP.objects.all()
    context = {'ip': ip, 'name': name,'allIp':allIp}
    try:
        ip = IP.objects.get(name=name)
    except:
        ip=IP()
    ip.name = name
    ip.ip = ip.save()
    return render(request, 'ip/index.html', context=context)
