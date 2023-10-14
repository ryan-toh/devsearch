from django.shortcuts import render
from .models import Profile, Skill, Message

# additional functions to import
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# import python file with helper functions (self-created)
from users.utils import searchProfiles

# import messages framework
from django.contrib import messages

# import customPaginator (self-created)
from users.utils import customPaginator

## MIGRATED TO FORMS.PY
# import forms framework so you don't have to create a form by yourself
# this is similar to a modelForm
# from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm

# for the Profiles view
RESULTS_PER_PAGE = 6

# Create your views here.

# ONBOARDING SECTION

# LOGGING IN, LOGGING OUT, REGISTRATION
def loginUser(request):
    # if a form was submitted
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username does not exist")

        # queries database for the username and password entered, returns None
        # if the user does not exist or password is incorrect
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # creates session for user in the database
            # add the session token into browser cookies
            login(request, user)
            return redirect('account')
        else:
            messages.error(request, 'Username or password incorrect')
    page = "login"
    context = {"page": page}
    return render(request, "users/login_onboarding.html", context)


def logoutUser(request):
    # deletes the current session
    logout(request)
    messages.info(request, "You have now logged out.")
    return redirect('login')


def onboardingUser(request):
    # if form submitted via POST
    if request.method == "POST":
        # pass in POST request and fill out form
        form = CustomUserCreationForm(request.POST)
        # submit the form to the database
        if form.is_valid():
            # commit=False holds a temporary instamce of it,
            # without saving to the database, so that you
            # can modify/verify the data if needed
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            messages.info(request, "Account successfully created!")
            return redirect("profile")
        else:
            messages.error(request, "Check that your inputs are valid. Please try again.")

    page = "register"
    # from the UserForms library, creates a template to render
    form = CustomUserCreationForm()
    context = {
        "page": page,
        "form": form,
               }
    return render(request, 'users/login_onboarding.html', context)

# PROFILE SECTION

# PROFILE LIST PAGE
def profiles(request):
    # get all the profiles in the database
    profile_list = Profile.objects.all()

    # get the query from the GET form
    q = ""
    if request.GET.get("search_query"):
        q = request.GET.get("search_query")
        profile_list = searchProfiles(q)

    # custom paginator
    profile_list, custom_range = customPaginator(request, profile_list, RESULTS_PER_PAGE)

    return render(request, "users/profiles.html", {"profile_list": profile_list, "search_query" : q, "custom_range": custom_range})


# INDIVIDUAL PROFILE PAGE
def indivProfile(request, pk):
    # show the user's account instead if they click on their own profile
    if request.user.is_authenticated: 
        if str(request.user.profile.id) == pk: 
            return redirect("account")
    profile_data = Profile.objects.get(id=pk)
    # exclude skills in the queryset if there is a blank "" expression
    featuredSkills = profile_data.skill_set.exclude(description__exact="")
    otherSkills = profile_data.skill_set.filter(description="")
    return render(request, "users/user_profile.html", {"profile_data": profile_data, "featuredSkills": featuredSkills, "otherSkills": otherSkills})


# PERSONAL PROFILE PAGE
@login_required(login_url="login")
def accountProfile(request):
    # get the login user by doing "request.user"
    # explaining the syntax: "request.user" is the UserModel for the user itself, ".profile" is the
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {"profile": profile, "skills": skills, "projects": projects}
    return render(request, "users/account.html", context)

# UPDATE PERSONAL PROFILE
@login_required(login_url="login")
def editAccount(request):
    # edit the user that is currently logged in
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        # request.FILES is needed so that you can receive images too
        if form.is_valid():
            print("Form registered valid.")
            form.save()

            # show the users' account again
            return redirect("account")

    # get current field data
    form = ProfileForm(instance=profile)
    context = {"form": form}
    return render(request, 'users/profile_form.html', context)

# SKILL SECTION

# EDIT SKILL FOR A PROFILE
@login_required(login_url=login)
def editSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    # if a form was submitted
    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill was edited successfully")
            return redirect("account")

    # create a new instance of the SkillForm
    form = SkillForm(instance=skill)
    context = {"form": form, "state": "update"}
    return render(request, 'users/skill_form.html', context)


# ADD SKILL FOR A PROFILE
@login_required(login_url=login)
def addSkill(request):
    profile = request.user.profile
    # if a form was submitted
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, "Skill was added successfully")
            return redirect("account")

    # create a new instance of the SkillForm
    form = SkillForm()
    context = {"form": form, "state": "add"}

    return render(request, 'users/skill_form.html', context)


# REMOVE SKILL FOR A PROFILE
@login_required(login_url=login)
def removeSkill(request, pk):
    profile = request.user.profile
    # if a form was submitted
    if request.method == "POST":
        skill = profile.skill_set.get(id=pk)
        skill.delete()
        messages.success(request, "Skill was removed successfully")
        return redirect("account")

    # this code does not currently work, the except does not 
    # catch when the skill is not found
    try:
        skill = profile.skill_set.get(id=pk)
        context = {"object": skill}
    except ValueError:
        context = {"object": ""}

    return render(request, 'users/remove_skill.html', context)

# MESSAGES SECTION

@login_required(login_url=login)
def messageInbox(request):
    profile = request.user.profile
    inbox = Message.objects.filter(recipient=profile)

    context = {
        "inbox": inbox,
        "unread": sum(not message.is_read for message in inbox)
    }
    return render(request, 'users/inbox.html', context)
        
@login_required(login_url=login)
def indivMessage(request, pk):
    # get the message details from the id of the message
    message = Message.objects.get(id=pk)
    message.is_read = True
    message.save()

    context = {"message": message}
    return render(request, 'users/message.html', context)


def createMessage(request, pk):
    if request.method == "POST":
        form = MessageForm(request.POST, is_authenticated=False)
        if form.is_valid():
            message = form.save(commit=False)
            message.recipient = Profile.objects.get(id=pk)
            if request.user.is_authenticated:
                message.sender = Profile.objects.get(id=request.user.profile.id)
                message.name = Profile.objects.get(id=request.user.profile.id).name
                message.email = Profile.objects.get(id=request.user.profile.id).email
            message.save()
            messages.success(request, "Your message was successfully sent.")
            return redirect("indivProfile", pk)

    messageForm = MessageForm(is_authenticated=request.user.is_authenticated)

    context = {"form": messageForm, "recipient": pk, "message_type": "new"}
    return render(request, 'users/message_form.html', context)


# template for this is the same as createMessage, only some parameters are changed to support navigation back into the user's inbox
@login_required(login_url=login)
def replyMessage(request, pk):
    messageForm = MessageForm(is_authenticated=True)

    context = {"form": messageForm, "recipient": pk, "message_type": "reply"}
    return render(request, 'users/message_form.html', context)


@login_required(login_url=login)
def deleteMessage(request, pk):
    profile = request.user.profile
    # if a form was submitted
    if request.method == "POST":
        message = Message.objects.get(id=pk)
        message.delete()
        messages.success(request, "Message deleted.")
        return redirect("inbox")

    # this code does not currently work, the except does not 
    # catch when the skill is not found
    try:
        message = Message.objects.get(id=pk)
        context = {"object": message}
    except ValueError:
        context = {"object": ""}

    return render(request, 'users/remove_skill.html', context)



