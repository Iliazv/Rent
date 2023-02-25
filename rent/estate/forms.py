from django import forms  
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Picture


class SignupForm(UserCreationForm):  
    email = forms.EmailField(max_length=200, help_text='Required')  
    class Meta:  
        model = get_user_model()
        fields = ('email', 'password1', 'password2')


class ImageForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ('annoucement', 'image')