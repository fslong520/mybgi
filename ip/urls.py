from django.urls import path

from ip import views

urlpatterns = [
    path('', views.index),
    path('<name>', views.saveIp),
]
