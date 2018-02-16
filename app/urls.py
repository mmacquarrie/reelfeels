"""emoticontent URL Configuration

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
from django.urls import path

import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('video', views.video_content),
    path('profile', views.user_profile),
    path('upload', views.upload_page),
    path('login', views.login_page),
    path('signup', views.signup_page),
    path('search', views.search_page),
    path('explore', views.explore_page)
]
