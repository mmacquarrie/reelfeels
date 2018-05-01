import datetime
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.template import Context
from .models import Video, Profile, Comment, ViewInstance
from django.db.models import F
from urllib.parse import parse_qs, urlparse
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, CommentCreationForm, VideoUpdateForm, LoginForm, VideoUploadForm, UserUpdateForm, ProfileUpdateForm
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist

import numpy as np
from numpy import trapz

time_offset = 3

def index(request):
    return render(request, 'index.html', {})

def calculus(one, two):
    arr = np.array([one,two])
    return trapz(arr, dx=time_offset)

def video_content(request, video_id):
    # if request is an AJAX POST request (and a user is currently logged in), update the ViewInstance (or create a new one if necessary)
    if(request.method == 'POST' and request.is_ajax() and request.user.is_authenticated):
        cur_video = Video.objects.get(id=video_id)
        currentView = None
        # Either get the ViewInstance or create it if it doesn't yet exist
        try:
            currentView = ViewInstance.objects.get(video_id=cur_video, viewer_id=request.user.profile)
        except ViewInstance.DoesNotExist:
            currentView = ViewInstance(video_id=cur_video, viewer_id=request.user.profile)

        # update the emotion values in currentView
        currentView.calculated_happiness += calculus(currentView.previous_happiness,int(request.POST.get('joy')) )
        currentView.previous_happiness = int(request.POST.get('joy'))
        currentView.calculated_sadness += calculus(currentView.previous_sadness,int(request.POST.get('sadness')) )
        currentView.previous_sadness = int(request.POST.get('sadness'))
        currentView.calculated_disgust += calculus(currentView.previous_disgust, int(request.POST.get('disgust')))
        currentView.previous_disgust = int(request.POST.get('disgust'))
        currentView.calculated_anger += calculus(currentView.previous_anger,int(request.POST.get('anger')) )
        currentView.previous_anger = int(request.POST.get('anger'))
        currentView.calculated_surprise += calculus(currentView.previous_surprise, int(request.POST.get('surprise')))
        currentView.previous_surprise = int(request.POST.get('surprise'))

        # set last_watched date to today
        currentView.last_watched = datetime.date.today()

        currentView.save()

        # Note: check admin site to view the updated ViewInstance for testing!!!

        return HttpResponse() #TO-DO: not really sure what to return here... (figure out if this is important!)

    # else, the request is not AJAX, and the page should be normally/synchronously rendered
    else:
        # Get video object from url
        video = get_object_or_404(Video, pk=video_id)

        #note that this references the profile, not the django user
        uploader = video.uploader_id

        if (request.user == uploader.user):
            is_owner = True
            edit_url = request.get_full_path() + "/edit"
            delete_url = request.get_full_path() + "/delete"
        else:
            is_owner = False
            edit_url = "" #throws errors otherwise
            delete_url = ""

        form = CommentCreationForm()

        # update global video stats from all the views for that video
        calculate_global_emotions(None, video)

        # increase video views by 1
        video.todays_views += 1
        video.save()

        # pass in the ViewInstance corresponding to the video and user (if it exists)
        user_view = None
        if (request.user.is_authenticated):
            try:
                user_view = ViewInstance.objects.get(video_id=Video.objects.get(id=video_id), viewer_id=request.user.profile)
            except ViewInstance.DoesNotExist:
                # do nothing
                pass

        return render(
            request,
            'video-content.html',
            context={
                'video': video,
                'form': form,
                'uploader': uploader,
                'comment_list': video.comment_set.all,
                "is_owner": is_owner,
                "edit_url": edit_url,
                "delete_url":delete_url,
                'view': user_view,
            }
        )

def user_profile(request, user_id):
    is_owner = (request.user.is_authenticated) and (user_id == request.user.id)
    profile = get_object_or_404(Profile, id=user_id)
    calculate_global_emotions(profile, None)

    return render(
        request,
        'user-profile.html',
        context={
            'user': profile,
            'is_owner': is_owner
        }
    )

def my_profile(request):
    profile = get_object_or_404(Profile, user_id=request.user.id)
    is_owner = (profile == request.user.profile)
    calculate_global_emotions(profile, None)

    return render(
        request,
        'user-profile.html',
        context={
            'user': profile,
            'is_owner': is_owner
        }
    )

# Generalized function for calculating a user/video's overall emotional stats
def calculate_global_emotions(profile, video):
    # Get views corresponding to profile/video in parameters
    if profile is not None and video is None:
        views = ViewInstance.objects.filter(viewer_id=profile)
        thing = profile
    elif video is not None and profile is None:
        views = ViewInstance.objects.filter(video_id=video)
        thing = video
    else:
        raise Http404()

    # Sum up all the emotion data for a given user/video and calculate the ratio of each emotion
    if(views.count() > 0):
        total_happy = total_sadness = total_disgust = total_anger = total_surprise = 0

        for view in views:
            total_happy += view.calculated_happiness
            total_sadness += view.calculated_sadness
            total_disgust += view.calculated_disgust
            total_anger += view.calculated_anger
            total_surprise += view.calculated_surprise

            total_emotions = total_happy + total_sadness + total_disgust + total_anger + total_surprise

            # Don't divide by 0, kids
            if (total_emotions > 0):
                thing.happiness = round((total_happy/total_emotions) * 100)
                thing.sadness = round((total_sadness/total_emotions) * 100)
                thing.disgust = round((total_disgust/total_emotions) * 100)
                thing.anger = round((total_anger/total_emotions) * 100)
                thing.surprise = round((total_surprise/total_emotions) * 100)
                thing.save()

def login_page(request):

    # If the user is already logged in
    if request.user.is_authenticated:
        return render(request, 'my-profile', {})

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = LoginForm(request.POST)

        if form.is_valid():
            form_data = form.cleaned_data
            user = authenticate(username=form_data.get('username'), password=form_data.get('password'))

            # A backend authenticated the credentials
            if user is not None:
                login(request, user)
                return redirect('explore')
            else:
                form = LoginForm()
                message = "Invalid credentials :( Try again"
                return render(request, 'login.html', {'form': form, 'message': message})

    # Else show form
    form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')

def signup_page(request):
    #If the form is being submitted, process it
    if request.user.is_authenticated:
        return redirect('my-profile')
    elif request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            # load the profile instance created by the signal in the profile model
            user.refresh_from_db()
            user.profile.profile_pic = form.cleaned_data.get('profile_pic')
            user.save()
            raw_password = form.cleaned_data.get('password1')

            #log the user in
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')

    #Otherwise, display a new sign up form
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {"form":form})

def upload_page(request):
    # if user is logged in, show the upload view
    if request.user.is_authenticated:
        # if user is submitting form
        if request.method == 'POST':
            form = VideoUploadForm(request.POST)
            #have to pop this error since video_url is handled in a specific way by upload.js (url is verified in browser, then video_url is in request.POST)
            form.errors.pop('video_url')
            if form.is_valid():
                new_video = Video()
                new_video.title = form.cleaned_data.get('video_title')
                new_video.video_link = request.POST.get('video_url')
                new_video.video_description = form.cleaned_data.get('video_description')
                new_video.uploader_id = request.user.profile
                new_video.date_shared = datetime.date.today()
                new_video.save()
                return redirect(reverse('video', args=[new_video.id]))

        # else if server is getting blank/default form for user to fill for the first time
        else:
            form = VideoUploadForm()
        return render(request, 'upload.html', {'form':form})
    # else if user is not logged in, take them to login view instead
    else:
        form = LoginForm()
        message = "You must log in to upload videos"
        return render(request, 'login.html', {'form': form, 'message': message})



def search_page(request):
    search_query = request.GET.get('search-query')

    if search_query == None:
        return render(request, 'explore.html', {})

    matching_videos = Video.objects.filter(title__icontains=search_query)

    return render(
        request,
        'search-results.html',
        context = {
            "matching_videos": matching_videos,
            "query": search_query,
        }
    )

def explore_page(request):
    # Get list of new videos
    new_cutoff = datetime.datetime.now() - datetime.timedelta(days=7)
    new_videos = Video.objects.filter(date_shared__gte=new_cutoff)

    # Get list of popular videos
    popular_videos = Video.objects.order_by("-todays_views")[:6]

    # Get list of controversial videos?
    return render(
        request,
        'explore.html',
        context={
            "new_videos": new_videos,
            "popular_videos": popular_videos,
        },
    )
class VideoUpdate(UpdateView):
    model = Video
    form_class = VideoUpdateForm
    template_name = 'video_update_form.html'

    def get_success_url(self):
        return reverse('video', kwargs={'video_id': self.object.id})

    def get_object(self, *args, **kwargs):
        obj = super(VideoUpdate, self).get_object(*args, **kwargs)
        if not obj.uploader_id.user == self.request.user:
            raise Http404()
        return obj

class VideoDelete(DeleteView):
    model = Video
    template_name = 'video_confirm_delete.html'

    def get_success_url(self):
        obj = super(VideoDelete, self).get_object()
        return reverse_lazy('my-profile')

    def get_object(self, *args, **kwargs):
        obj = super(VideoDelete, self).get_object(*args, **kwargs)
        if not obj.uploader_id.user == self.request.user:
            raise Http404()
        return obj

def update_profile(request):
    if request.user.is_authenticated:
        if (request.method == 'POST'):

            user_form = UserUpdateForm(request.POST, instance=request.user)
            profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

            if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save()
                user.set_password(user_form.cleaned_data.get('password'))
                user.save()
                profile_form.save()

                if user is not None:
                    login(request, user)
                    return redirect('my-profile')

        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

        return render(request, 'user-update-form.html', {
            'user_form' : user_form,
            'profile_form' : profile_form
        })

    else:
        form = LoginForm()
        message = "You must log in to update your account"
        return render(request, 'login.html', {'form': form, 'message': message})

class CommentHandler:
    def add_comment(request, video_id):
        video = get_object_or_404(Video, pk=video_id)

        if request.method == 'POST' and request.user.is_authenticated:
            form = CommentCreationForm(request.POST)

            if form.is_valid():
                form_data = form.cleaned_data
                new_comment = Comment()
                new_comment.video_id = video
                new_comment.commenter_id = request.user.profile
                new_comment.content = form_data.get('comment')
                new_comment.save()

        return redirect("video", video_id)

    def delete_comment(request, video_id, comment_id):
        video = get_object_or_404(Video, pk=video_id)
        comment = get_object_or_404(Comment, pk=comment_id)

        if request.method == 'POST' and request.user.is_authenticated:
            if request.user == comment.commenter_id.user:
                comment.delete()

        return redirect("video", video_id)
