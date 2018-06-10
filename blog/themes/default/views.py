import configparser
import os

from django.shortcuts import render

from blog.models import Article, Column, Comment, User


class Config(object):
    def __init__(self, configPath):
        config = configparser.ConfigParser()
        try:
            config.read(configPath)
            self.blog = {}
            self.user = {}
            self.blog['name'] = config.get('blog', 'name')
            self.user['name'] = config.get('user', 'name')
            self.user['intro'] = config.get('user', 'intro')
        except:
            self.blog = None
            self. user = None


def setConfigList():
    path = os.path.dirname(os.path.abspath(__file__))
    configPath = os.path.join(path, 'config.ini')
    config = Config(configPath)
    if config.blog:
        configList = [config.blog['name'],
                      config.user['name'], config.user['intro'], ]
    else:
        configList = ''
    return configList


configList = setConfigList()


def getAllArticle():
    try:
        return Article.objects.all()
    except:
        return None


def getAllUser():
    try:
        return User.objects.all()
    except:
        return None


def getAllColumn():
    try:
        return Column.objects.all()
    except:
        return None


def getAllComment():
    try:
        return Comment.objects.all()
    except:
        return None


def index(request):
    context = {'config': configList, 'articles': getAllArticle()}
    return render(request, 'index.html', context=context)

# Create your views here.
