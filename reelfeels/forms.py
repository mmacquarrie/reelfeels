from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import Video, Profile, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class' : 'form-control required'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control required'}))

class SignUpForm(UserCreationForm):
    profile_pic = forms.ImageField(required=False)
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Email', 'class' : 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username', 'class' : 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class' : 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class' : 'form-control'}))

    class Meta:
        model = User
        fields = ('profile_pic','username', 'email','password1', 'password2')


#creating the form to allow users to create new comments
class CommentCreationForm(forms.Form):
    comment = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Submit a public comment', 'size': '100', 'maxlength':'1000'}))

# form class for uploading a video
class VideoUploadForm(forms.Form):
    video_url = forms.URLField(widget=forms.URLInput(attrs={'class':'form-control', 'placeholder':'YouTube URL...', 'id':'video-url-input'}))
    video_title = forms.CharField(label='Title:', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Upload Title...'}))
    video_description = forms.CharField(label='Description:', widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Upload Description...', 'id':'upload-desc', 'maxlength':'1000', 'rows':'5'}))


class VideoUpdateForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ( 'title', 'video_description')
        widgets = {
            'title': forms.Textarea(attrs={'cols': 10, 'rows': 2, 'class': 'form-control'}),
            'video_description': forms.Textarea(attrs={'cols': 10, 'rows': 10, 'class': 'form-control'}),
        }
        labels = {
            'title': _('Title'),
            'video_description': _('Description'),
        }

    def clean(self):
        cleaned_data = super(VideoUpdateForm, self).clean()

        title = cleaned_data.get('title')
        video_description = cleaned_data.get('video_description')

        return cleaned_data

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_pic', )