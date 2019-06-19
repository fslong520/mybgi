from django.db import models

# Create your models here.
class IP(models.Model):
    objects = models.Manager()
    name = models.CharField('姓名', max_length=255, default='匿名')
    ip =models.TextField('IP', default='//127.0.0.1')
    regTime=models.DateTimeField('注册时间', auto_now_add=True)

    class Meta:
        verbose_name = 'IP'
        #verbose_name_pliral = '标签'
        ordering = ['regTime']

    def __str__(self):
        return self.name