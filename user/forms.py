from typing import Any
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms


class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "avatar", "bio", "password1", "password2"]
        widgets = {
            "avatar": forms.FileInput()
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username", "avatar", "bio"]
        widgets = {
            "avatar": forms.FileInput()
        }
    