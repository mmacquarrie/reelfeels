# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Video, Profile, Comment, ViewInstance

# Video class
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'video_link', 'video_description', 'todays_views')
    list_filter = ('title', 'todays_views')

# User class
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'id')
    list_filter = ('user',)

# VideoToUser
# admin.site.register(Upload)
admin.site.register(Comment)
admin.site.register(ViewInstance)
