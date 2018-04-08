from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
    
class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Profile
    