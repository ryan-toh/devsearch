from django.contrib import admin

# Register your models here.

# add your model here
from .models import Project, Tag, Review

# show Project on the admin panel
admin.site.register(Project)
admin.site.register(Tag)
admin.site.register(Review)