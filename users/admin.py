from django.contrib import admin

# Register your models here.
# add your model here
from .models import Profile, Skill, Message

# show Project on the admin panel
admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Message)