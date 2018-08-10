from django.urls import path

from apis import views

urlpatterns = [
    path('bingpic', views.getBingPic),
    path('getWeather', views.getWeather),
    path('test',views.test),
    path('searchBooks',views.searchBooks),
    path('wallpaper',views.getTodayWallpaper)
]
