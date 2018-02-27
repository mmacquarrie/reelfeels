# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import uuid

# Videos
class Video(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4().hex[:8], editable=False, max_length=8)

    title = models.TextField(max_length=100, help_text='Insert video title here', verbose_name='Title')

    video_link = models.TextField(verbose_name='Link to Video', max_length=1000, help_text='Insert video link here')
    video_description = models.TextField(max_length=1000, verbose_name="Video Description", null=True)

    happiness = models.IntegerField(verbose_name='Global happiness', default=0)
    sadness = models.IntegerField(verbose_name='Global sadness', default=0)
    disgust = models.IntegerField(verbose_name='Global disgust', default=0)
    anger = models.IntegerField(verbose_name='Global anger', default=0)
    surprise = models.IntegerField(verbose_name='Global surprise', default=0)

    date_shared = models.DateField(blank=False)
    last_updated = models.DateField(blank=False)

    total_views = models.IntegerField(verbose_name='Total views', default=0)

    user_id = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        ordering = ["-date_shared"]

    def __str__(self):
        return self.title

def profile_filename(instance, filename):
    return 'static/profile_pictures/user_{0}/{1}'.format(instance.id, filename)

# Users
class User(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4().hex[:8], editable=False, max_length=8)

    date_joined = models.DateField(verbose_name='Date Joined', blank=False)

    username = models.CharField(max_length=50)

    # TO-DO: decide where to put uploaded files
    profile_pic = models.FileField(upload_to=profile_filename, null=True, blank=True,)

    # TO-DO: figure out how to use encryption to store passwords

    happiness = models.IntegerField(verbose_name='Overall happiness', default=0)
    sadness = models.IntegerField(verbose_name='Overall sadness', default=0)
    disgust = models.IntegerField(verbose_name='Overall disgust', default=0)
    anger = models.IntegerField(verbose_name='Overall anger', default=0)
    surprise = models.IntegerField(verbose_name='Overall surprise', default=0)

    date_updated_emotions = models.DateField(verbose_name='When overall emotions were last calculated', blank=True, null=True)

# Emotions for certain videos
class VideoToUser(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4().hex[:8], editable=False, max_length=8)

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    video_id = models.ForeignKey(Video, on_delete=models.CASCADE)

    date_updated = models.DateField(verbose_name='Date updated', blank=False)

    happiness = models.IntegerField(verbose_name='Happiness', default=0)
    sadness = models.IntegerField(verbose_name='Sadness', default=0)
    disgust = models.IntegerField(verbose_name='Disgust', default=0)
    anger = models.IntegerField(verbose_name='Anger', default=0)
    surprise = models.IntegerField(verbose_name='Surprise', default=0)

# Comment for a given video, made by a given user
class Comment(models.Model):
    # I copied the id from the other tables above -- is this fine for comments?
    id = models.CharField(primary_key=True, default=uuid.uuid4().hex[:8], editable=False, max_length=8)

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    video_id = models.ForeignKey(Video, on_delete=models.CASCADE)

    # TO-DO: decide what (if any) the max_length of a single comment should be
    text = models.TextField(max_length=1000, help_text='Write your comment here!', verbose_name='The text content of a comment')
