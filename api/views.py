# Libraries required for the django REST framework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import ProjectSerializer
from projects.models import Project, Review, Tag

from django.http import JsonResponse


@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'GET': '/api/projects'},
        {'GET': '/api/projects/id'},
        {'POST': '/api/projects/id/vote'},

        # API authentication
        {'POST': '/api/users/token'},

        # refresh users' token to stay logged in
        {'POST': '/api/users/token/refresh'},
    ]

    
    return Response(routes)


@api_view(['GET'])
# # ABOUT @PERMISSION_CLASSES
# # analagous to "login_required", except that we are using JSON webtokens instead of sessions here
# # TIP: if isAuthenticated is required, add the key "Authorization" with value "Bearer <insertAccessToken>"
# # You may get the access token by using api/users/token (token will be generated from login credentials)
# # P.S. we use "Bearer" as it is specifed as a keyword under AUTH_HEADER_TYPES in settings.py under SIMPLE_JWT
# @permission_classes([IsAuthenticated])
def getProjects(request):
    print("USER:", request.user)
    # DO NOT DO THIS: RESPONSE() REQUIRES SERIALIZED (JSON-IFIED) DATA
    # projects = Project.objects.all()
    # return Response(projects)

    projects = Project.objects.all()
    # many=True as you want to serialize ALL the projects in the queryset
    serializer = ProjectSerializer(projects, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def getProject(request, pk):
    # DO NOT DO THIS: RESPONSE() REQUIRES SERIALIZED (JSON-IFIED) DATA
    # projects = Project.objects.all()
    # return Response(projects)

    projects = Project.objects.get(id=pk)
    # many=False as you want to serialize only 1 project in the queryset
    serializer = ProjectSerializer(projects, many=False)

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request, pk):
    # the request is now coming from the JWT instead of the session token
    user = request.user.profile

    # POST request information
    data = request.data
    project = Project.objects.get(id=pk)
    review, created = Review.objects.get_or_create(
        owner = user,
        project = project,
    )
    try:
        review.body = data["body"]
        if data["value"] == "up" or data["value"] == "down":
            review.value = data["value"]
        else:
            raise ValueError
    except KeyError:
        return JsonResponse({"ErrorName":"KeyError",
                            "ErrorDesc":"Incorrect or missing Key. Key name should be 'body' and 'value'."
                            })
    except ValueError:
        return JsonResponse({"ErrorName":"ValueError",
                            "ErrorDesc":"Incorrect Value. Format should be <value:'up' or 'down'>."
                            })

    try:
        project.vote_total += 1
        if data["value"] == "up":
            project.vote_positive += 1          
            project.vote_ratio = (project.vote_positive / project.vote_total) * 100
        elif data["value"] == "down":
            project.vote_ratio = (project.vote_positive / project.vote_total) * 100
        else:
            return JsonResponse({"ErrorName": "NameError",
                             "ErrorDesc":"Incorrect Value. Format should be <value: 'up' or 'down'>.",
                             })
    except KeyError:
        return JsonResponse({"ErrorName": "KeyError",
                             "ErrorDesc":"Incorrect or missing Key. Key name should be 'value'.",
                             })
    finally:
        # created returns True or False
 

        project.save()

    serializer = ProjectSerializer(project, many=False)

    return Response(serializer.data)


@api_view(['DELETE'])
def removeTag(request):
    tagId = request.data["tagId"]
    projectId = request.data["projectId"]

    project = Project.objects.get(id=projectId)
    tag = Tag.objects.get(id=tagId)

    project.tags.remove(tag)

    return Response("Tag removed from project")