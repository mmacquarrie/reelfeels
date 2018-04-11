import datetime
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import Context
from .models import Video, Profile, Comment
from django.db.models import F
from urllib.parse import parse_qs, urlparse
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, CommentCreationForm, VideoUpdateForm, UserRegistrationForm

def index(request):
    return render(request, 'index.html', {})

def video_content(request, video_id):
    # Get video object from url
    video = get_object_or_404(Video, pk=video_id)

    #note that this references the profile, not the django user
    uploader = video.uploader_id

    if (request.user == uploader.user):
        is_owner = True
        edit_url = request.get_full_path() + "/edit"
    else:
        is_owner = False
        edit_url = "" #throws errors otherwise

    #form content
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentCreationForm(request.POST)

        if form.is_valid():
            form_data = form.cleaned_data
            new_comment = Comment()
            new_comment.video_id = video
            new_comment.commenter_id = request.user.profile
            new_comment.content = form_data.get('comment')
            new_comment.save()


            #create a new comment using video, and the content from the form also need to get the comment creators  id
    #form content

    form = CommentCreationForm()

    return render(
        request,
        'video-content.html',
        context={
            'video': video,
            'form': form,
            # TO-DO:
            # current user's stats displayed in 'Your stats' tab...
            # 'your_happiness':cur_user.happiness,
            # 'your_sadness':cur_user.sadness,
            # 'your_disgust':cur_user.disgust,
            # 'your_surprise':cur_user.surprise,
            # 'your_anger':cur_user.anger,
            'uploader': uploader,
            'comment_list': video.comment_set.all,
            "is_owner": is_owner,
            "edit_url": edit_url,
        }
    )

def user_profile(request, user_id):
    profile = get_object_or_404(Profile, id=user_id)

    return render(
        request,
        'user-profile.html',
        context={
            'user': profile,
        }
    )

def login_page(request):

    # If the user is already logged in
    if request.user.is_authenticated:
        return(request, 'index.html', {})

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        print('Post request received')

        # Create a form instance and populate it with data from the request (binding):
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form_data = form.cleaned_data
            user = authenticate(username=form_data.get('username'), password=form_data.get('password'))

            # A backend authenticated the credentials
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form = UserRegistrationForm()
                message = "Invalid credentials :( Try again"
                return render(request, 'login.html', {'form': form, 'message': message})

    # Else show form
    form = UserRegistrationForm()
    return render(request, 'login.html', {'form': form})

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')

def signup_page(request):
    #If the form is being submitted, process it
    if request.method == 'POST':
        form = SignUpForm(request.POST)
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

    if request.user.is_authenticated:
        return render(request, 'upload.html', {})
    else:
        form = UserRegistrationForm()
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
            "matching_videos": matching_videos
        }
    )

def explore_page(request):
    # Get list of new videos
    new_cutoff = datetime.datetime.now() - datetime.timedelta(days=7)
    new_videos = Video.objects.filter(date_shared__gte=new_cutoff)

    # Get list of popular videos
    popular_videos = Video.objects.order_by("-todays_views")[:10]

    # Get list of controversial videos?
    return render(
        request,
        'explore.html',
        context={
            "new_videos": new_videos,
            "popular_videos": popular_videos,
        },
    )

def video_edit(request, video_id):
    video = get_object_or_404(Video, pk=video_id)

    #If the user is trying to edit a video they own, proceed. Otherwise, deny access.
    if (request.user == video.uploader_id.user):
        form = VideoUpdateForm()
        return render(request, "video_update_form.html", {})
    else:
        return render(request, "access_denied.html", {})
