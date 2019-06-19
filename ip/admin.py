from django.contrib import admin

from ip import models as IpModels
# Register your models here.



class IpInfo(admin.ModelAdmin):
    list_display = ['id','name', 'ip', 'regTime' ]
    list_filter = ['regTime','name']
    search_fields = ['name','ip']


admin.site.register(IpModels.IP,IpInfo)
# Register your models here.
