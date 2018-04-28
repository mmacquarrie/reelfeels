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

def index(request):
    return render(request, 'index.html', {})

def video_content(request, video_id):
    # if request is an AJAX POST request (and a user is currently logged in), update the ViewInstance (or create a new one if necessary)
    if(request.method == 'POST' and request.is_ajax() and request.user.is_authenticated):
        #print(request.POST)
        cur_video = Video.objects.get(id=video_id)
        currentView = None
        # Either get the ViewInstance or create it if it doesn't yet exist
        try:
            currentView = ViewInstance.objects.get(video_id=cur_video, viewer_id=request.user.profile)
        except ViewInstance.DoesNotExist:
            currentView = ViewInstance(video_id=cur_video, viewer_id=request.user.profile)
        
        # update the emotion values in currentView
        # Note: currently just adding values to the view... (CHANGE THIS BEHAVIOR???)
        currentView.happiness += int(request.POST.get('joy'))
        currentView.sadness += int(request.POST.get('sadness'))
        currentView.disgust += int(request.POST.get('disgust'))
        currentView.anger += int(request.POST.get('anger'))
        currentView.surprise += int(request.POST.get('surprise'))

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
        return render(request, 'my-profile', {})

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
        print("hello 2")

        print(request.method)

        if request.method == 'POST' and request.user.is_authenticated:
            print("hello1")
            if request.user == comment.commenter_id.user:
                print("hello")
                comment.delete()

        return redirect("video", video_id)
