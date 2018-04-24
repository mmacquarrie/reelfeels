from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('video', views.video_content, name='video-static'),
    path('video/<video_id>', views.video_content, name='video'),
    path('my-profile', views.my_profile, name='my-profile'),
    path('profile/update', views.update_profile, name='profile-update'),
    path('profile/<user_id>', views.user_profile, name='profile'),
    path('upload', views.upload_page, name='upload'),
    path('login', views.login_page, name='login'),
    path('signup', views.signup_page, name='signup'),
    path('search', views.search_page, name='search'),
    path('explore', views.explore_page, name='explore'),
    path('logout', views.logout_page, name='logout'),
    path('video/<pk>/edit', views.VideoUpdate.as_view(), name='video-edit'),
    path('video/<pk>/delete', views.VideoDelete.as_view(), name='video-delete'),
]