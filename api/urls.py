from django.urls import path
from . import views

# for JSON web token authentication
# third party framework
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('', views.getRoutes),
    path('projects/', views.getProjects),
    path('projects/<str:pk>/', views.getProject),
    path('projects/vote/<str:pk>/', views.projectVote),

    # for JSON web token authentication
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Tokens are stored on the browser 

    # EXTENSION TO DEVSEARCH: THIS IS USED TO DELETE EXISTING TAGS FROM A PROJECT
    # DO NOT REMOVE: MAY BREAK PROJECT_FORM
    path('remove-tag/', views.removeTag),
]