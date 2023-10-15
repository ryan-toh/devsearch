# importing required models
from django.contrib.auth.models import User
from .models import Profile, Skill

# import the post_save signal (for profileUpdated)
from django.db.models.signals import post_save, post_delete, pre_delete

# importing a decorator function for your signal so you don't have to use
# the connect function to connect "post_save" or other signal to your function
from django.dispatch import receiver

# to send emails to the user (make sure you have configured parameters to use email)
from django.core.mail import send_mail
from django.conf import settings

# ** When using signals in a seperate file like this,
# tell django in apps.py

# DJANGO SIGNALS - READ MORE ABOUT THEM IN ATTACHED DJANGO NOTES

# sender - model that sent the signal
# instance - instance of model that triggered this
# created - if a new model was added to database (true/false)

# METHOD 2: USING @RECEIVER
@receiver(post_save, sender=Profile)
def profileUpdated(sender, instance, created, **kwargs):
    print("Profile Saved.")
    print("Database Instance:", instance)
    print(f"Instance was {'new' if created else 'not new'}")

@receiver(post_delete, sender=Profile)
def profileDeleted(sender, instance, **kwargs):
    print(f"{instance} has been deleted. See you again!")

@receiver(pre_delete, sender=Skill)
def skillDeleted(sender, instance, **kwargs):
    print(f"deleted skill {instance}")

# METHOD 1: USING CONNECT()
# tells django to trigger profileUpdated after chosen model is saved
# post_save.connect(profileUpdated, sender=Profile)
# post_delete.connect(profileDeleted, sender=Profile)

# next idea - use a signal to create a Profile for a newly created User
@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs):
    # if a new model was created, aka created == True
    if created:
        user = instance
        profile = Profile.objects.create(
            # set the param user to
            # the user that was just created
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name
            # the above attributes can be obtained
            # by looking at the Django docs for User
        )

        subject = "Welcome to Devsearch"
        message = "We are glad you are here!"

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,

        )

# signal to delete a User if a Profile is erased
@receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    if instance:
        print(f"The User {instance} was also deleted, along with its profile")
        user = instance.user
        user.delete()

# signal to update a User if a Profile is updated
@receiver(post_save, sender=Profile)
def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    # to avoid createProfile from triggering upon save
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()
        print(f"The User '{instance}' was updated, as its Profile was updated.")

# error occurs when you delete user

# expected behaviour: when user deleted, profile deleted

# current issue: deletion of user, deletes profile but as such, triggers deletion of the user again

