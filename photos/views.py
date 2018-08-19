from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse

# Create your views here.

def index(request):
    context = {}
    return render(request, 'webapps/index.html', context=context)