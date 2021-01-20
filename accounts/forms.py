from django import forms
from . models import Profile
from django.contrib.auth.models import User

class SignUpForm(forms.Form):
    username = forms.CharField(max_length=250)
    firstname = forms.CharField(max_length=250)
    lastname = forms.CharField(max_length=250)
    password = forms.CharField(widget=forms.PasswordInput)
    bio = forms.CharField(max_length=200,required=False)
    email = forms.EmailField(max_length=254,required=False)