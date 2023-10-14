from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from projects.models import Project, Review, Tag
from users.models import Profile
from projects.forms import ProjectForm, ReviewForm

# import messages framework
from django.contrib import messages

# user must be signed in to access certain pages
from django.contrib.auth.decorators import login_required

# import the Q lookup library
from django.db.models import Q
from django.db import IntegrityError

# import helper function (self-created)
from projects.utils import searchProjects, customPaginator

RESULTS_PER_PAGE = 6

# pass in a Request object
def projects(request):
    proj_list = Project.objects.all()
    q = ""
    if request.GET.get("search_query"):
        q = request.GET.get("search_query")
        proj_list = searchProjects(q)

    # pagination of projects

    proj_list, custom_range = customPaginator(request, proj_list, RESULTS_PER_PAGE)

    # we can do this as we already told django where
    # to find the html files in settings.py using path
    return render(request, "projects/projects.html", {"list": proj_list, "search_query": q, "custom_range": custom_range})

    # the path to find is templates/projects/<file>.html


def project(request, pk):
    # to process and add a review
    projectObj = Project.objects.get(id=pk)
    profile = request.user.profile
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            # verify that the project belongs to the current user
            current_user = profile.id
            project_owner = projectObj.owner.id

            if current_user == project_owner:
                messages.error(request, "Permission Error: Can't review a project owned by you.")
                return redirect("project", pk)
            try:
                # process review and add info
                review = form.save(commit=False)
                review.owner = profile
                review.project = projectObj

                # validating and adding votes to project
                if form.cleaned_data["value"] == "up":
                    projectObj.vote_positive += 1
                
                projectObj.vote_total += 1
                projectObj.vote_ratio = (projectObj.vote_positive / projectObj.vote_total) * 100

                projectObj.save()

                print("Total Votes:", projectObj.vote_total, "Positive Votes:", projectObj.vote_positive)

                review.save()
                messages.success(request, "Review published.")
                return redirect("project", pk)
            except IntegrityError:
                # IntegrityError raised when the UNIQUE constraint fails
                # User may only publish one review for one project (see Review in models.py)
                messages.error(request, "You have already reviewed this project.")


    try:
        project = Project.objects.get(id=pk)
    except ValueError:
        return HttpResponse("Project not found. If you believe this is an error, please send feedback and we will look into it.")
    
    # to display project details
    proj_data = {
        "title": project.title,
        "tags": project.tags.all(),
        "featured_image": project.featured_image,
        "description": project.description if project.description else "No project description",
        "demo_link": project.demo_link,
        "source_link": project.source_link,
        "vote_total": project.vote_total,
        "vote_ratio": project.vote_ratio,
        "owner": Profile.objects.get(username=project.owner).name,
        "owner_id": Profile.objects.get(username=project.owner).id,
    }

    # to display project reviews
    reviews = project.review_set.all()

    review_data = []
    for review in reviews:
        review_data.append({
            "name": Profile.objects.get(id=review.owner.id).name,
            "image": Profile.objects.get(id=review.owner.id).profile_image,
            "id": Profile.objects.get(id=review.owner.id).id,
            "body": review.body,
        })

    return render(request, "projects/single_project.html", {"proj_data": proj_data, "review_data": review_data, "review_form": ReviewForm()})


# if not login, redirect to login page
@login_required(login_url="login")
def create_project(request):
    profile = request.user.profile
    # if a form was submitted
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            # creates a new object and adds it to the Project model automatically
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            messages.success(request, "Project successfully created")
            # redirect accepts the url path name defined in urlpatterns
            return redirect("account")

    context = {'form': ProjectForm(), 'state': 'create'}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def update_project(request, pk):
    try:
        project = Project.objects.get(id=pk)
    except ValueError:
        return HttpResponse("Project not found. If you believe this is an error, please send feedback and we will look into it.")

    # verify that the project belongs to the current user
    current_user = request.user.profile.id
    project_owner = project.owner.id

    if current_user != project_owner:
        messages.error(request, "Permission Error: You are not the owner of this project. Sign in to the correct account and try again.")
        return redirect("projects")

    # if a form was submitted
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            # creates a new object and adds it to the Project model automatically
            form.save()
            messages.success(request, "Project successfully edited.")
            # redirect accepts the url path name defined in urlpatterns
            return redirect("account")

    # allows you to modify this specific projects' data when calling 'instance'
    form = ProjectForm(instance=project)
    context = {'form': form, 'state': 'update'}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def delete_project(request, pk):
    if request.method == "POST":
        try:
            Project.objects.get(id=pk).delete()
            return redirect("account")
        except ValueError:
            return HttpResponse("Project not found. No project deleted. If you believe this is an error, please send feedback and we will look into it.")

    try:
        project = Project.objects.get(id=pk)
    except ValueError:
        return HttpResponse("Project not found. If you believe this is an error, please send feedback and we will look into it.")

    return render(request, "projects/delete_object.html", {"object": project})
