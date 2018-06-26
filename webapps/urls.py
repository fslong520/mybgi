from django.urls import path
from webapps import views

urlpatterns = [
    path('', views.index),
    path('getBingPicUrl',views.getBingPicUrl),
    path('getVideo',views.getVideo),
]