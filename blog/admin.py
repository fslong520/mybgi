from django.contrib import admin
from blog import models as blogModels


class ArticleInfo(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'column', 'pubTime', ]
    list_filter = ['column']
    search_fields = ['title']


admin.site.register(blogModels.Article,ArticleInfo)
admin.site.register(blogModels.Column)
admin.site.register(blogModels.User)
admin.site.register(blogModels.Comment)
# Register your models here.
