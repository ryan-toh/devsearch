# created seperately from the original django files
# used to store all the models used for forms

from django.forms import ModelForm
from django import forms
from .models import Profile, Skill, Message
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# by convention, suggested syntax is <ModelName>Form
# ONBOARDING FORM
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        # search the django docs for the name of the built in fields
        # password1: password
        # password2: confirm password
        fields = ["first_name", "email", "username", "password1", "password2"]
        labels = {
            "first_name" : "Name",
            "email": "Email",
        }

    # to override and add a css attribute to each UserCreationForm field
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


# UPDATE USER INFORMATION FORM
class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'username', 'location', 'bio', 'short_intro',
                  'profile_image', 'social_github', 'social_twitter',
                  'social_linkedin', 'social_youtube', 'social_website']

    # to override and add a css attribute to each UserCreationForm field
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


# UPDATE SKILL INFORMATION FORM
class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = ["name", "description"]

    # to override and add a css attribute to each UserCreationForm field
    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


# CREATE MESSAGE FORM
class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']

    def __init__(self, *args, **kwargs):
        is_authenticated = kwargs.pop('is_authenticated')
        super(MessageForm, self).__init__(*args, **kwargs)

        if is_authenticated:
            del self.fields['name']
            del self.fields['email']

        for name, fields in self.fields.items():
            fields.widget.attrs.update({'class': 'input'})


