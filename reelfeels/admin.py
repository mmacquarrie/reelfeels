# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Video, User, Upload, Comment, ViewInstance

# Video class
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'video_link', 'todays_views')
    list_filter = ('title', 'todays_views')

# User class
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'id', 'date_joined')
    list_filter = ('username', 'date_joined')

# VideoToUser
admin.site.register(Upload)
admin.site.register(Comment)
admin.site.register(ViewInstance)
