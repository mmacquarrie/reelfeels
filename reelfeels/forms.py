from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import Video, Profile
    
class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class' : 'form-control required'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control required'}))
   