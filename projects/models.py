from django.db import models
import uuid
from users.models import Profile

# Create your models here.
# create classes that represent tables, as shown below
"""
EXAMPLE

# "models.Model" tells django that it is a database model, not just a class
class Project(models.Model):
    # this simultes the CREATE TABLE command in sqlite3
    title = models.CharField()
    description = models.TextField()
    id = models.UUIDField()

"""

class Project(models.Model):
    # connect a project to a given user
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    # max length is required for each charfield
    title = models.CharField(max_length=200)

    # allowed to create a row in the database without a description if null=True
    # for POST request, allowed to submit a row without a description if blank=True
    description = models.TextField(null=True, blank=True)

    # allows the model to store an image
    featured_image = models.ImageField(
        null=True, blank=True, default="default.jpg"
    )

    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)

    # allows a project to have multiple tags
    # note: you can pass in the name of the class 'Tag', or if already defined
    tags = models.ManyToManyField('Tag', blank=True)


    vote_positive = models.IntegerField(default=0, null=True, blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    # timestamp on when proj added
    # auto_now_add generates timestamp upon upload to database
    created = models.DateTimeField(auto_now_add=True)
    # encoding type is uuid4
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    # how the class represents itself when you print the class as a string
    # (by default, it is the memory address where the class is)
    def __str__(self):
        return self.title
    
    # sort projects according to specified criterion
    class Meta:
        # the data will be ordered according to the attribute "created"
        # as defined in the Profile model
        # "-" flips the order it is arranged
    # EXAMPLE
        # "created" sorts from oldest to newest
        # "-created" sorts from newest to oldest

        ordering = ["-created"]


class Review(models.Model):
    VOTE_TYPE = (
        ("up", "Upvote"),
        ("down", "Downvote"),
                 )
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    # when a project is deleted, on_delete=models.SET_NULL
    # will delete project key but leave all other params intact
    # on_delete=models.CASCADE will delete all entires with the project key
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(max_length=200, null=True, blank=True)
    # the choices parameter will enforce a dropdown (use a tuple to add options)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    # encoding type is uuid4
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    

    class Meta:
        # ensures that you can only leave one review for one project
        unique_together = [['owner', 'project']]


    def __str__(self):
        return self.value


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name














