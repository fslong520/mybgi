from django.urls import path

from apis import views

urlpatterns = [
    path('bingpic', views.getBingPic),
    path('getweather', views.getWeather),
    path('test',views.test)
]
