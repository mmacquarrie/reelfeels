from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context
from .models import Video, User
import datetime
from django.db.models import F

def index(request):
    return render(request, 'index.html', {})

def video_content(request, video_id):
    #get video object from url
    video = Video.objects.get(pk='06aec4dc')#video_id)

    uploader = User.objects.get(pk='240ee468')#video.uploader_id)
    user_photo_path = uploader.profile_pic.url

    return render(
        request,
        'video-content.html',
        context={
            'video_code':video.video_link,
            'happiness':video.happiness,
            'sadness':video.sadness,
            'disgust':video.disgust,
            'surprise':video.surprise,
            'anger':video.anger,

            # TO-DO:
            # current user's stats displayed in 'Your stats' tab...
            """
            'your_happiness':uploader.happiness,
            'your_sadness':uploader.sadness,
            'your_disgust':uploader.disgust,
            'your_surprise':uploader.surprise,
            'your_anger':uploader.anger,
            """

            'user_photo_path':user_photo_path,
            'uploader_name':uploader.username,
            'video_desc':video.video_description,
            'upload_date':video.date_shared,
            'comment_list':video.comment_set.all,
        })

def user_profile(request):
    return render(request, 'user-profile.html', {})

def login_page(request):
    return render(request, 'login.html', {})

def signup_page(request):
    return render(request, 'signup.html', {})

def upload_page(request):
    return render(request, 'upload.html', {})

def search_page(request):
    return render(request, 'search-results.html', {})

def explore_page(request):
    # get list of new videos
    new_cutoff = datetime.datetime.now() - datetime.timedelta(days=7)
    new_videos = Video.objects.filter(date_shared__gte=new_cutoff)

    # get list of popular videos
    popular_videos = Video.objects.filter(todays_views__gte=F('yesterdays_views')*1.5)

    # get list of controversial videos?
    return render(
        request,
        'explore.html',
        context={
            "new_videos":new_videos,
            "popular_videos":popular_videos,
        },
    )
