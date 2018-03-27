from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import Context
from .models import Video, User
import datetime
from django.db.models import F
from urllib.parse import parse_qs, urlparse

def index(request):
    return render(request, 'index.html', {})

def video_content(request, video_id):
    #get video object from url
    video = get_object_or_404(Video, pk=video_id)

    uploader = video.uploader_id
    print(uploader.profile_pic.url)

    return render(
        request,
        'video-content.html',
        context={
            'video': video,

            # TO-DO:
            # current user's stats displayed in 'Your stats' tab...
            # 'your_happiness':cur_user.happiness,
            # 'your_sadness':cur_user.sadness,
            # 'your_disgust':cur_user.disgust,
            # 'your_surprise':cur_user.surprise,
            # 'your_anger':cur_user.anger,

            # 'uploader_image':uploader.user_image,
            'uploader': uploader,
            'comment_list':video.comment_set.all,
        })

def user_profile(request, user_id):
    profile=get_object_or_404(User, pk=user_id)

    return render(
        request,
        'user-profile.html',
        context={'user':profile,}
    )

def login_page(request):
    return render(request, 'login.html', {})

def signup_page(request):
    return render(request, 'signup.html', {})

def upload_page(request):
    return render(request, 'upload.html', {})

def search_page(request):
    search_query = request.GET.get('search-query')

    if search_query == None:
        return render(request, 'explore.html', {})

    matching_videos = Video.objects.filter(title__icontains=search_query)

    return render(
        request,
        'search-results.html',
        context = {
            "matching_videos":matching_videos
        }
    )

def explore_page(request):
    # get list of new videos
    new_cutoff = datetime.datetime.now() - datetime.timedelta(days=7)
    new_videos = Video.objects.filter(date_shared__gte=new_cutoff)

    # get list of popular videos
    popular_videos = Video.objects.order_by("-todays_views")[:10]

    # get list of controversial videos?
    return render(
        request,
        'explore.html',
        context={
            "new_videos":new_videos,
            "popular_videos":popular_videos,
        },
    )
