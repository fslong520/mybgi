import configparser
import os

import markdown
from django.shortcuts import render

from blog.models import Article, Column, Comment, User
from django.http.response import HttpResponseRedirect, HttpResponse

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
            self.blog = {}
            self.user = {}
            self.blog['name'] = '明月不归尘'
            self.user['name'] = 'fslong'
            self.user['intro'] = '君子藏器于身，待时而动'
            self.user['profilePhoto'] = '//tva1.sinaimg.cn/crop.318.608.1137.1137.180/3c1b9c69jw8f1ptze8k4hj21kw1ekakh.jpg'


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
        comments = Comment.objects.filter(article=article)
        # comments.objects.order_by('pubTime')
        i = 1
        for comment in comments:
            comment.floor = i
            i += 1
        comments = mdToHtml(comments)
    except:
        comments = None
    try:
        username = request.session.get('name')
        user = User.objects.get(name=username)
    except:
        username = None
        user = None
    context = {'config': configList,
               'articles': articles, 'comments': comments, 'user': user, }
    return render(request, 'blogs.html', context=context)


# 创建文章：
def createAritcle(request):
    if request.method == 'POST':
        username = request.session.get('name')
        user = User.objects.get(name=username)
        article = Article()
        title = request.POST.get('title')
        author = request.POST.get('author')
        content = request.POST.get('content')
        columnname = request.POST.get('column')
        column = Column.objects.get(name=columnname)
        article.author = author
        article.title = title
        article.content = content
        article.column = column
        article.user = user
        article.save()
        articles = mdToHtml([article])
        try:
            comments = Comment.objects.filter(article=article)
            # comments.objects.order_by('pubTime')
            i = 1
            for comment in comments:
                comment.floor = i
                i += 1
            comments = mdToHtml(comments)
        except:
            comments = None
        context = {'config': configList,
                   'articles': articles, 'comments': comments, 'user': user, 'message': '新增文章成功，你今天的每份努力，明天都会获得更多，加油！'}
        return render(request, 'blogs.html', context=context)
    else:
        username = request.session.get('name')
        try:
            user = User.objects.get(name=username)
        except:
            user = None
        columns = getAllColumn()
        context = {'config': configList, 'user': user, 'columns': columns, }
        return render(request, 'createArticle.html', context=context)


# 创建评论：
def createComment(request):
    if request.method == 'POST':
        username = request.session.get('name')
        articleid = request.POST.get('articleid', '')
        content = request.POST.get('commentText', '')
        comment = Comment()
        user = User.objects.get(name=username)
        article = Article.objects.get(id=articleid)
        comment.user = user
        comment.article = article
        comment.content = content
        comment.save()
        comment.floor = len(Comment.objects.filter(article=article))+1
        articles = mdToHtml([article])
        comments = Comment.objects.filter(article=article)
        # comments.objects.order_by('pubTime')
        i = 1
        for comment in comments:
            comment.floor = i
            i += 1
        comments = mdToHtml(comments)
        context = {'config': configList,
                   'articles': articles, 'comments': comments, 'user': user, 'message': '评论发表成功！'}
        return render(request, 'blogs.html', context=context)

    else:
        context = {'config': configList, }
        return render(request, 'index.html', context=context)


# 登陆页面：
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        articleid = request.POST.get('articleid', '')
        try:
            user = User.objects.get(name=username)
            if user.password == password:
                request.session['name'] = username
                message = '登陆成功，你现在拥有了一些神奇能力！'
            else:
                message = '密码错了呢！'
        except:
            message = '呀，你还没注册呢！'
        finally:
            article = Article.objects.get(id=articleid)
            articles = mdToHtml([article])
            try:
                comments = Comment.objects.filter(article=article)
                # comments.objects.order_by('pubTime')
                i = 1
                for comment in comments:
                    comment.floor = i
                    i += 1
            except:
                comments = None
            try:
                username = request.session.get('name')
                user = User.objects.get(name=username)
            except:
                username = None
                user = None
            comments = mdToHtml(comments)
            context = {'config': configList,
                       'articles': articles, 'comments': comments, 'user': user, 'message': message}
            return render(request, 'blogs.html', context=context)


# 注册页面：
def register(request):
    username = request.POST.get('usernameReg', '')
    password = request.POST.get('passwordReg', '')
    email = request.POST.get('emailReg', '')
    profilePhoto = request.POST.get('profilePhoto', '')
    articleid = request.POST.get('articleid', '')
    if username == '' or password == '' or email == '':
        message = '输入错误了，快说你是怎么进的这个页面！'
    else:
        if profilePhoto == '':
            profilePhoto = '/static/img/deafaultprofilePhoto.png'
        user = User()
        user.name = username
        user.password = password
        user.email = email
        user.profilePhoto = profilePhoto
        try:
            userInDB = User.objects.get(name=username)
        except:
            userInDB = None
        if userInDB:
            message = '非常抱歉，你已经注册过了！'
        else:
            user.save()
            message = '哈哈！注册成功了啦（原谅老夫的少女心）！'
            request.session['name'] = user.name
    article = Article.objects.get(id=articleid)
    articles = mdToHtml([article])
    try:
        comments = Comment.objects.filter(article=article)
        i = 1
        for comment in comments:
            comment.floor = i
            i += 1
    except:
        comments = None
    try:
        username = request.session.get('name')
        user = User.objects.get(name=username)
    except:
        username = None
        user = None
    comments = mdToHtml(comments)
    context = {'config': configList,
               'articles': articles, 'comments': comments, 'user': user, 'message': message}
    return render(request, 'blogs.html', context=context)


# 用户总览：
def manage(request):
    message = request.GET.get('message', '')
    sessionName = request.session.get('name')
    try:
        user = User.objects.get(name=sessionName)
    except:
        user = None
    if user:
        try:
            articles = Article.objects.filter(user=user)
            comments = Comment.objects.filter(user=user)
            lens = [len(articles), len(comments)]
        except:
            articles = None
            comments = None
            lens = None
    else:
        articles = None
        comments = None
        lens = None
    for comment in comments:
        if len(comment.content) > 30:
            comment.content = comment.content[0:30]+'...'
    comments = mdToHtml(comments)
    context = {'config': configList, 'user': user,
               'articles': articles, 'comments': comments, 'lens': lens, 'message': message}
    return render(request, 'manage.html', context=context)


# 注销：
def signout():
    message = '注销成功，谢谢使用！'
    articles = getAllArticle()
    # 截断文章显示：
    for article in articles:
        if len(article.content) > 300:
            article.content = article.content[0:300]+'...'
    # 逆序排序文章：
    articles = articles[::-1]
    articles = mdToHtml(articles)
    context = {'config': configList, 'message': message, 'articles': articles}
    return context


# 管理用户：
def manageUser(request):
    action = request.POST.get('manageFunction',)
    action = action.strip()
    if action == 'signOut':
        request.session['name'] = None
        context = signout()
        return render(request, 'index.html', context=context)
    elif action == 'changePassword':
        message = '首先请使用原密码进行认证！'
        changePassword = True
        context = {'config': configList, 'message': message,
                   'changePassword': changePassword}
        return render(request, 'manageUser.html', context=context)
    elif action == 'changeProfilePhoto':
        message = '首先请使用原密码进行认证！'
        changeProfilePhoto = True
        context = {'config': configList, 'message': message,
                   'changeProfilePhoto': changeProfilePhoto, }
        return render(request, 'manageUser.html', context=context)
    else:
        message = '欢迎使用！'
        articles = getAllArticle()
        # 截断文章显示：
        for article in articles:
            if len(article.content) > 300:
                article.content = article.content[0:300]+'...'
        # 逆序排序文章：
        articles = articles[::-1]
        articles = mdToHtml(articles)
        context = {'config': configList,
                   'message': message, 'articles': articles}
        return render(request, 'index.html', context=context)


# 修改密码：
def changePassword(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    newPassword = request.POST.get('newPassword', None)
    if username:
        try:
            user = User.objects.get(name=username)
            if user.password == password:
                request.session['name'] = username
                user.password = newPassword
                user.save()
                return HttpResponse(True)
            else:
                return HttpResponse(False)
        except:
            return HttpResponse(False)
    else:
        return HttpResponse(False)


# 修改头像：
def changeProfilePhoto(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    newProfilePhoto = request.POST.get('newProfilePhoto', None)
    if username:
        try:
            user = User.objects.get(name=username)
            if user.password == password:
                request.session['name'] = username
                user.profilePhoto = newProfilePhoto
                user.save()
                return HttpResponse(True)
            else:
                return HttpResponse(False)
        except:
            return HttpResponse(False)
    else:
        return HttpResponse(False)


# 修改文章页：
def manageBlogEdit(request, id):
    if request.method == "POST":
        username = request.session.get('name')
        user = User.objects.get(name=username)
        article = Article.objects.get(id=id)
        title = request.POST.get('title')
        author = request.POST.get('author')
        content = request.POST.get('content')
        columnname = request.POST.get('column')
        column = Column.objects.get(name=columnname)
        try:
            article.author = author
            article.title = title
            article.content = content
            article.column = column
            article.save()
            return HttpResponse(True)
        except:
            return HttpResponse(False)
    else:
        sessionName = request.session.get('name')
        try:
            user = User.objects.get(name=sessionName)
        except:
            user = None
        article = Article.objects.get(id=id)
        message = '修改文章！'
        columns = getAllColumn()
        for i in range(len(columns)):
            if columns[i] == article.column:
                columnid = i
        context = {'config': configList,
                   'message': message, 'article': article, 'user': user, 'columns': columns, 'columnid': columnid, }
        return render(request, 'manageBlogEdit.html', context=context)


def deleteBlog(request, id):
    article = Article.objects.get(id=id)
    article.delete()
    return HttpResponseRedirect('/blog/manage?message=删除成功，谢谢！')


def deleteComment(request):
    id = request.POST.get('id')
    comment = Comment.objects.get(id=id)
    comment.delete()
    return HttpResponse('评论删除成功！')


def getArticleByColumn(request):
    columnname = request.GET.get('column')
    if columnname == 'others':
        articles = getAllArticle()
        others = []
        for article in articles:
            if article.column.name not in ['博客', '随笔']:
                others.append(article)
        articles = others
    else:
        column = Column.objects.get(name=columnname)
        articles = Article.objects.filter(column=column)
    # 截断文章显示：
    for article in articles:
        if len(article.content) > 300:
            article.content = article.content[0:300]+'...'
    # 逆序排序文章：
    articles = articles[::-1]
    articles = mdToHtml(articles)
    context = {'config': configList, 'articles': articles}
    return render(request, 'index.html', context=context)
