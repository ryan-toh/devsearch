# import required models
from .models import Skill, Profile

# import the Q lookup library
from django.db.models import Q

# import paginator class (for customPaginator)
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def searchProfiles(q):
    # SEARCH BY SKILLS
    # match the query to a skill in db
    # after matching, find profile (see below) with the skill in db
    skills = Skill.objects.filter(name__icontains=q)

    # SEARCH BY PROFILE
    # __icontains means find name where case insensitive, part of the string
    # use qlookup to expand our search criteria
    # "|" represents OR, "&" represents AND
    profile_list = Profile.objects.distinct().filter(
        Q(name__icontains=q) |
        Q(short_intro__icontains=q)|
        Q(skill__in=skills)
        )
    
    return profile_list


def customPaginator(request, list, results_per_page):
    """
    request: pass in request parameter
    list: A list of <querySet> objects for pagination
    results_per_page: the number of objects displayed per page
    """
    try:
        page_number = int(request.GET.get("page"))
    except:
        page_number = 1

    paginator = Paginator(list, results_per_page)
    try:
        list = paginator.page(page_number)
    except PageNotAnInteger:
        page_number = 1
        # default page is the first page
        list = paginator.page(page_number)
    except EmptyPage:
        page_number = 1
        # defualt to last page if page range exceeded
        # proj_list = paginator.page(paginator.num_pages)
        # OR default to first page
        list = paginator.page(page_number)

    # adding a custom range
    leftIndex = page_number - 4
    
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = page_number + 5

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    # show 10 indices even when page is less than 5
    if rightIndex < 10 and paginator.num_pages > 9:
        rightIndex = 10

    custom_range = range(leftIndex, rightIndex)

    return list, custom_range
