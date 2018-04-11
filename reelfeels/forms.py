from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import Video, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
    
class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class' : 'form-control required'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control required'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control required'
            })

class SignUpForm(UserCreationForm):
    profile_pic = forms.ImageField(required=False)
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = User
        fields = ('profile_pic','username', 'email','password1', 'password2')



#creating the form to allow users to create new comments
from .models import Comment

class CommentCreationForm(forms.Form):
    comment = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Submit a public comment', 'size': '100', 'maxlength':'1000'}))

    class Meta:
        model = Comment
        fields = ('content')    

# form class for uploading a video
class VideoUploadForm(forms.Form):
    video_url = forms.URLField(widget=forms.URLInput(attrs={'class':'form-control', 'placeholder':'YouTube URL...', 'id':'video-url-input'}))
    video_title = forms.CharField(label='Title:', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Upload Title...'}))
    video_description = forms.CharField(label='Description:', widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Upload Description...', 'id':'upload-desc', 'maxlength':'1000', 'rows':'5'}))