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

# built in views for password management (change/reset password)
from django.contrib.auth import views as auth_views

# urlpatterns shows how a user navigates a website and route them
urlpatterns = [
    # a URL path
    path("admin/", admin.site.urls),
    # go into projects/urls to find the urlpatterns from there
    path("", include('projects.urls')),
    path("profile/", include('users.urls')),

    # password reset form
    # IMPORTANT: KEEP THE PATH NAME AS "RESET_PASSWORD" as django looks out for them

    # view to enter email and confirm that reset email is sent
    path("reset_password/", auth_views.PasswordResetView.as_view(template_name="reset_password.html"), name="reset_password"),
    path("password_reset_sent/", auth_views.PasswordResetDoneView.as_view(template_name="reset_password_sent.html"), name="password_reset_done"),

    # view for the reset link sent via email
    path("reset/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view(template_name="reset.html"), name="password_reset_confirm"),

    # confirms password was reset
    path("password_reset_complete", auth_views.PasswordResetCompleteView.as_view(template_name="reset_complete.html"), name="password_reset_complete")
]

# create a url for our static files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# required URLs

"""
password_change
password_change_done

password_reset
password_reset_done

password_reset_confirm
password_reset_complete

"""
