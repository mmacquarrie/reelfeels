from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('video', views.video_content, name='video-static'),
    #path('video/<uuid>', views.video_content, name='video'),
    path('profile', views.user_profile, name='profile-static'),
    #path('profile/<uuid>', views.user_profile, name='profile'),
    path('upload', views.upload_page, name='upload'),
    path('login', views.login_page, name='login'),
    path('signup', views.signup_page, name='signup'),
    path('search', views.search_page, name='search'),
    path('explore', views.explore_page, name='explore'),
]
