# Generated by Django 2.0.5 on 2018-06-18 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20180618_2014'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='floor',
            field=models.IntegerField(default='0', verbose_name='楼层'),
        ),
    ]
