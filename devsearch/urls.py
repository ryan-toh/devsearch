"""
URL configuration for devsearch project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# navigation URL for the entire project
from django.contrib import admin
from django.urls import path, include
# allows us access to settings
from django.conf import settings
# helps us create a url for our static file
from django.conf.urls.static import static

# urlpatterns shows how a user navigates a website and route them
urlpatterns = [
    # a URL path
    path("admin/", admin.site.urls),
    # go into projects/urls to find the urlpatterns from there
    path("", include('projects.urls')),
    path("profile/", include('users.urls')),
]

# create a url for our static files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
