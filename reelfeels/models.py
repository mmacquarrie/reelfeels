# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import uuid
import datetime
from urllib.parse import urlparse
from urllib.parse import parse_qs
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Videos
class Video(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.TextField(max_length=100, help_text='Insert video title here', verbose_name='Title', default='An Emotional Video!')

    video_link = models.TextField(verbose_name='Link to Video', max_length=1000, help_text='Insert video link here')
    video_description = models.TextField(max_length=1000, verbose_name="Video Description", default='Am I happy? Sad? Disgusting?? Watch me to find out!')

    happiness = models.IntegerField(verbose_name='Global happiness', default=0)
    sadness = models.IntegerField(verbose_name='Global sadness', default=0)
    disgust = models.IntegerField(verbose_name='Global disgust', default=0)
    anger = models.IntegerField(verbose_name='Global anger', default=0)
    surprise = models.IntegerField(verbose_name='Global surprise', default=0)

    last_updated_emotions = models.DateField(null=True, default=datetime.date.today)

    yesterdays_views = models.IntegerField(verbose_name='Yesterdays views', default=0)

    todays_views = models.IntegerField(verbose_name='Todays views', default=0)

    date_shared = models.DateField(blank=False)

    #not in our diagram, but we need some reference to the uploader(User model)
    uploader_id = models.ForeignKey('Profile', on_delete=models.CASCADE)

    class Meta:
        ordering = ["-date_shared"]
        permissions = (
            ("can_edit", "Can edit video"),
        )

    def __str__(self):
        return self.title

    def get_youtube_thumbnail(self):
        return "http://i4.ytimg.com/vi/" + self.video_link + "/0.jpg"

    def get_top_emotion(self):
        emotions = {"none": 0, "happiness": self.happiness, "sadness":self.sadness,
            "disgust":self.disgust, "anger":self.anger, "surprise":self.surprise}
        return max(emotions, key=lambda key: emotions[key])

# TO-DO: find a way to delete this without it breaking (or just check if deleting this is magically okay now)
def profile_filename():
    return 'I exist because there is a weird migration conflict when I am not here'

# Users
class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='user')
    # TO-DO: decide where to put uploaded files
    profile_pic = models.ImageField(upload_to='profile_pictures/', null=True, blank=True, default = 'profile_pictures/default.png')

    happiness = models.IntegerField(verbose_name='Overall happiness', default=0)
    sadness = models.IntegerField(verbose_name='Overall sadness', default=0)
    disgust = models.IntegerField(verbose_name='Overall disgust', default=0)
    anger = models.IntegerField(verbose_name='Overall anger', default=0)
    surprise = models.IntegerField(verbose_name='Overall surprise', default=0)

    last_updated_emotions = models.DateField(verbose_name='When overall emotions were last calculated', blank=True, null=True)

    def get_username(self, obj):
        return obj.user.username

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

    def __str__(self):
        return self.user.__str__()

    def get_top_emotion(self):
        emotions = {"none": 0, "happiness": self.happiness, "sadness":self.sadness,
            "disgust":self.disgust, "anger":self.anger, "surprise":self.surprise}
        return max(emotions, key=lambda key: emotions[key])

# Emotions for certain videos
class ViewInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    viewer_id = models.ForeignKey('Profile', on_delete=models.CASCADE)
    video_id = models.ForeignKey('Video', on_delete=models.CASCADE)

    last_watched = models.DateField(verbose_name='Date updated', blank=False)

    happiness = models.IntegerField(verbose_name='Happiness', default=0)
    sadness = models.IntegerField(verbose_name='Sadness', default=0)
    disgust = models.IntegerField(verbose_name='Disgust', default=0)
    anger = models.IntegerField(verbose_name='Anger', default=0)
    surprise = models.IntegerField(verbose_name='Surprise', default=0)

# Comment for a given video, made by a given user
class Comment(models.Model):
    # I copied the id from the other tables above -- is this fine for comments?
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    video_id = models.ForeignKey('Video', on_delete=models.CASCADE)
    commenter_id = models.ForeignKey('Profile', on_delete=models.CASCADE)

    # TO-DO: decide what (if any) the max_length of a single comment should be
    content = models.TextField(max_length=1000, help_text='Write your comment here!', verbose_name='The text content of a comment')

    def __str__(self):
        return self.content


"""
# The uploads
class Upload(models.Model):
    # I copied the id from the other tables above -- is this fine for uploads?
    id = models.CharField(primary_key=True, default=uuid.uuid4().hex[:8], editable=False, max_length=8)

    video_id = models.OneToOneField('Video', on_delete=models.CASCADE)

    uploader = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return '"{0}" -- {1}'.format(self.video_id, self.uploader)
"""