from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import UserProfile

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2', 'first_name',
                  'middle_name', 'last_name']


class UserLoginForm(forms.Form):
    username_or_email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['about_me', "profile_picture", "phone_number", "address", "resume"]
