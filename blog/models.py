from django.db import models

# Create your models here.


class User(models.Model):
    objects = models.Manager()
    name = models.CharField('姓名', max_length=255, default='匿名')


class Article(models.Model):
    objects = models.Manager()
    titile = models.CharField('标题', max_length=255, default='无主题')
    user = models.ForeignKey(
        User, on_delete=models.SET_DEFAULT, default='匿名用户')


class Column(models.Model):
    objects = models.Manager()
    name = models.CharField('栏目', max_length=255, default='杂')


class Comment(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(
        User, on_delete=models.SET_DEFAULT, default='匿名用户')
