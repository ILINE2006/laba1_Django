from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Question


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    avatar = forms.ImageField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'avatar']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'short_description', 'full_description', 'image']
        widgets = {
            'short_description': forms.Textarea(attrs={'rows': 3}),
            'full_description': forms.Textarea(attrs={'rows': 5}),
        }