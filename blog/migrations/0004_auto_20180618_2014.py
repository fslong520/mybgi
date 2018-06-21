# Generated by Django 2.0.5 on 2018-06-18 12:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_user_profilephoto'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='changeTime',
            field=models.DateTimeField(auto_now=True, verbose_name='修改时间'),
        ),
        migrations.AddField(
            model_name='comment',
            name='pubTime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='发表时间'),
            preserve_default=False,
        ),
    ]