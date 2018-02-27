# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Video, User, VideoToUser, Comment

# Video class
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'video_link', 'total_views')
    list_filter = ('title', 'total_views')

# User class
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'id', 'date_joined')
    list_filter = ('username', 'date_joined')

# VideoToUser
admin.site.register(VideoToUser)
admin.site.register(Comment)
