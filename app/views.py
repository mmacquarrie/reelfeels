from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context

def index(request):
    return render(request, 'index.html', {})

def video_content(request):
    return render(request, 'video-content.html', {})

def user_profile(request):
    return render(request, 'user-profile.html', {})