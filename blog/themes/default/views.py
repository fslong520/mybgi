import configparser
import os

import markdown
from django.shortcuts import render

from blog.models import Article, Column, Comment, User

# Create your views here.


# 将article里的markdown翻译成html
def mdToHtml(articles):
    exts = ['markdown.extensions.abbr', 'markdown.extensions.admonition', 'markdown.extensions.attr_list', 'markdown.extensions.codehilite', 'markdown.extensions.def_list', 'markdown.extensions.extra', 'markdown.extensions.fenced_code', 'markdown.extensions.footnotes',
            'markdown.extensions.headerid', 'markdown.extensions.meta', 'markdown.extensions.nl2br', 'markdown.extensions.sane_lists', 'markdown.extensions.smart_strong', 'markdown.extensions.smarty', 'markdown.extensions.tables', 'markdown.extensions.toc', 'markdown.extensions.wikilinks']
    for article in articles:
        article.content = markdown.markdown(article.content, extensions=exts)
    return articles
# 配置信息的类：


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
            self.user['profilePhoto'] = config.get(
                'user', 'profilePhoto')
        except:
            self.blog = None
            self. user = None


# 设置配置信息的函数：
def setConfigList():
    path = os.path.dirname(os.path.abspath(__file__))
    configPath = os.path.join(path, 'config.ini')
    config = Config(configPath)
    if config.blog:
        configList = [config.blog['name'],
                      config.user['name'], config.user['intro'], config.user['profilePhoto']]
    else:
        configList = ''
    return configList


configList = setConfigList()


# 获取所有文章：
def getAllArticle():
    try:
        return Article.objects.all()
    except:
        return None


# 获取所有用户：
def getAllUser():
    try:
        return User.objects.all()
    except:
        return None


# 获取所有栏目：
def getAllColumn():
    try:
        return Column.objects.all()
    except:
        return None


# 获取所有评论：
def getAllComment():
    try:
        return Comment.objects.all()
    except:
        return None


# 首页：
def index(request):
    articles = getAllArticle()
    # 截断文章显示：
    for article in articles:
        if len(article.content) > 300:
            article.content = article.content[0:300]+'...'
    # 逆序排序文章：
    articles = articles[::-1]
    articles = mdToHtml(articles)
    context = {'config': configList, 'articles': articles}
    return render(request, 'index.html', context=context)


# 根据文章id获取文章：
def getArticleById(request, id):
    try:
        article = Article.objects.get(id=id)
    except:
        article = None
    articles = mdToHtml([article])
    try:
        comment = Comment.objects.filter(article=article)
    except:
        comment = None
    context = {'config': configList,
               'articles': articles, 'comment': comment, }
    return render(request, 'blogs.html', context=context)


# 创建文章：
def createAritcle(request):
    context = {'config': configList,
               'users': getAllUser(), 'columns': getAllColumn()}
    return render(request, 'createArticle.html', context=context)
