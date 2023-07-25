from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.core.exceptions import ValidationError

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

    # def clean(self):
    #     p1 = self.cleaned_data.get('password1')
    #     p2 = self.cleaned_data.get('password2')
    #     if p1 != p2:
    #         raise ValidationError("P1 ")

    def clean_profile_picture(self):
        pp = self.cleaned_data.get('profile_picture')
        if pp:
            extension = pp.name.split(".")[-1]  # picture.jpg  = ["picture", "jpg"]
            if extension.lower() not in ['jpg', 'png', "jpeg", 'svg']:
                raise ValidationError("Profile Picture Must Be In Image Format !!")
        return pp

    def clean_resume(self):
        resume = self.cleaned_data.get('profile_picture')
        if resume:
            extension = resume.name.split(".")[-1]  # resume.pdf  = ["resume", "pdf"]
            if extension.lower() != 'pdf':
                raise ValidationError("Resume Must Be In PDF Format !!")
        return resume
