from django.db import models
# this is the UserModel that django built for us
from django.contrib.auth.models import User
import uuid


# Create your models here.

class Profile(models.Model):
    # a user can only have one profile,
    # and a profile belongs to one user only.
    # "User" is Django's built in model.
    # when a user gets deleted, delete the entry here too
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=False, null=False)
    email = models.EmailField(max_length=500, blank=False, null=False)
    username = models.CharField(max_length=200, blank=False, null=False)
    location = models.CharField(max_length=200, blank=True, null=True)
    short_intro = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    # django finds the static folder, then navigate to the "profiles" directory and uploads it there
    profile_image = models.ImageField(null=True, blank=True, upload_to='profiles/', default='profiles/user-default.png')
    social_github = models.CharField(max_length=200, blank=True, null=True)
    social_twitter = models.CharField(max_length=200, blank=True, null=True)
    social_linkedin = models.CharField(max_length=200, blank=True, null=True)
    social_youtube = models.CharField(max_length=200, blank=True, null=True)
    social_website = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        # str() ensures that self.username is a string
        return str(self.username)
    
        # sort profiles according to specified criterion
    class Meta:
        # the data will be ordered according to the attribute "created"
        # as defined in the Profile model
        # "-" flips the order it is arranged
    # EXAMPLE
        # "created" sorts from oldest to newest
        # "-created" sorts from newest to oldest

        ordering = ["-created"]

class Skill(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=False, null=False)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)
    

class Message(models.Model):
    # SET_NULL is used so that the recipient can see their messages after sender deletes account
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)

    # by using "related_name", we can access the messages model thru the Profile model using just "Profile.messages" instead of "Profile.messages_set"
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()

    # boolean to see if recipient read the message
    is_read = models.BooleanField(default=False, null=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.subject
    
    class Meta:
        ordering = ["is_read", "-created"]







