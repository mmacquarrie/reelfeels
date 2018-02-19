from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('video', views.video_content),
    path('profile', views.user_profile),
    path('upload', views.upload_page),
    path('login', views.login_page),
    path('signup', views.signup_page),
    path('search', views.search_page),
    path('explore', views.explore_page)
]


