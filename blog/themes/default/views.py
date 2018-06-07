import configparser
import os

from django.shortcuts import render
path = os.path.dirname(os.path.abspath(__file__))


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


def index(request):
    configPath = os.path.join(path, 'config.ini')
    config = Config(configPath)
    if config.blog:
        configList = [config.blog['name'],
                      config.user['name'], config.user['intro'], ]
    else:
        configList = ''
    context = {'config': configList, }
    return render(request, 'index.html', context=context)

# Create your views here.
