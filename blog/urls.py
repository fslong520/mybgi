"""mybgi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from blog.themes.default import views as themesViews

urlpatterns = [
    path('', themesViews.index),
    path('<int:id>', themesViews.getArticleById),
    path('ca', themesViews.createAritcle),
    path('cc', themesViews.createComment),
    path('signin', themesViews.signin),
    path('signout', themesViews.signout),
    path('manage', themesViews.manage),
    path('reg', themesViews.register),
    path('mu', themesViews.manageUser),
    path('deleteComment', themesViews.deleteComment),
    path('editBlog/<int:id>', themesViews.manageBlogEdit),
    path('deleteBlog/<int:id>', themesViews.deleteBlog),
    path('changePassword', themesViews.changePassword),
    path('changeProfilePhoto', themesViews.changeProfilePhoto),
    path('blogsByColumn', themesViews.getArticleByColumn),
    path('search',themesViews.getArticleByKeyWords),

]
