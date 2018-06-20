from django.db import models

# Create your models here.


class User(models.Model):
    objects = models.Manager()
    name = models.CharField('姓名', max_length=255, default='匿名')
    email = models.EmailField('Email', max_length=255,
                              default='test@example.cpm')
    password = models.CharField('密码', max_length=255, default='admin')
    profilePhoto = models.TextField(
        '头像', default='//tva1.sinaimg.cn/crop.318.608.1137.1137.180/3c1b9c69jw8f1ptze8k4hj21kw1ekakh.jpg')
    isAdmin = models.BooleanField('管理员权限', default=False)
    regTime=models.DateTimeField('注册时间', auto_now_add=True)

    class Meta:
        verbose_name = '小伙伴'
        #verbose_name_pliral = '标签'
        ordering = ['name']

    def __str__(self):
        return self.name


class Column(models.Model):
    objects = models.Manager()
    name = models.CharField('栏目', max_length=255, default='杂')

    class Meta:
        verbose_name = '栏目'

    def __str__(self):
        return self.name


class Article(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(
        User, on_delete=models.SET_DEFAULT, default=1)
    column = models.ForeignKey(
        Column, on_delete=models.SET_DEFAULT, default=1)
    title = models.CharField('标题', max_length=255, default='无主题')
    pubTime = models.DateTimeField('发表时间', auto_now_add=True)
    changeTime = models.DateTimeField('修改时间', auto_now=True)
    author = models.CharField('作者', max_length=255, default='佚名')
    content = models.TextField('内容', default='')

    class Meta:
        verbose_name = '文章'
        #verbose_name_pliral = '文章'
        ordering = ['pubTime']

    def __str__(self):
        return ('%s(作者：%s)' % (self.title, self.author))


class Comment(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(
        User, on_delete=models.SET_DEFAULT, default=1)
    article = models.ForeignKey(
        Article, on_delete=models.SET_DEFAULT, default=1)
    content = models.TextField('评论', default='')
    pubTime = models.DateTimeField('发表时间', auto_now_add=True)
    changeTime = models.DateTimeField('修改时间', auto_now=True)
    floor = models.IntegerField('楼层', default='0')

    class Meta:
        verbose_name = '评论'
        ordering = ['pubTime']

    def __str__(self):
        return self.content
