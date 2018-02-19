from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context

def index(request):
    return render(request, 'index.html', {})

def video_content(request):
    return render(request, 'video-content.html', {})

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
    return render(request, 'explore.html', {})