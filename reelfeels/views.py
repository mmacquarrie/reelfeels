import datetime
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.template import Context
from .models import Video, Profile, Comment
from django.db.models import F
from urllib.parse import parse_qs, urlparse
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, CommentCreationForm, VideoUpdateForm, LoginForm, VideoUploadForm, UserUpdateForm, ProfileUpdateForm
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView

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
        delete_url = request.get_full_path() + "/delete"
    else:
        is_owner = False
        edit_url = "" #throws errors otherwise
        delete_url = ""

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
            "delete_url":delete_url,
        }
    )

def user_profile(request, user_id):
    is_owner = (request.user.is_authenticated) and (user_id == request.user.id)
    profile = get_object_or_404(Profile, id=user_id)
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
    print (is_owner)
    return render(
        request,
        'user-profile.html',
        context={
            'user': profile,
            'is_owner': is_owner
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
        form = LoginForm(request.POST)

        if form.is_valid():
            form_data = form.cleaned_data
            user = authenticate(username=form_data.get('username'), password=form_data.get('password'))

            # A backend authenticated the credentials
            if user is not None:
                login(request, user)
                return redirect('home')
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
    if request.method == 'POST':
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
class VideoUpdate(UpdateView):
    model = Video
    form_class = VideoUpdateForm
    template_name = 'video_update_form.html'

    def get_initial(self):
        if self.uploader_id.user != self.request.user:
            return HttpResponseForbidden()
        else:
            initial = super(VideoUpdate, self).get_initial()

            # retrieve current object
            video_object = self.get_object()

            initial['title'] = video_object.title
            initial['video_description'] = video_object.video_description


            return initial

    def get_success_url(self):
        return reverse('video', args={},    kwargs={'video_id': self.object.id})

class VideoDelete(DeleteView):
    model = Video
    template_name = 'video_confirm_delete.html'

    def get_object(self, queryset=None):
        obj = super(VideoDelete, self).get_object()
        if not obj.uploader_id.user == self.request.user:
            return HttpResponseForbidden()
        return obj

    def get_success_url(self):
        obj = super(VideoDelete, self).get_object()
        return reverse_lazy('profile', args=[obj.uploader_id.id])


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
                return redirect('profile', args=[request.user.id])

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
