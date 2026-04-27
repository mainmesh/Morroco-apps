from django import forms
from django.contrib.auth.models import User

from .models import Profile


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Email Address')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    location = forms.CharField(required=False, max_length=100, label='Location')

    class Meta:
        model = Profile
        fields = ['location']
