# add paths relating to the parent route "/users"

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('onboarding/', views.onboardingUser, name="onboarding"),

    path("", views.profiles, name="profile"),
    path("profile/<str:pk>", views.indivProfile, name="indivProfile"),

    path("account/", views.accountProfile, name="account"),
    path("edit-account/", views.editAccount, name="edit-account"),

    path("edit-skill/<str:pk>", views.editSkill, name="edit-skill"),
    path("add-skill", views.addSkill, name="add-skill"),
    path("remove-skill/<str:pk>", views.removeSkill, name="remove-skill"),

    path("inbox/", views.messageInbox, name="inbox"),
    path("inbox/<str:pk>", views.indivMessage, name="indivMessage"),
    path("create-message/<str:pk>", views.createMessage, name="createMessage"),
    path("reply-message/<str:pk>", views.replyMessage, name="replyMessage"),
    path("delete-message/<str:pk>", views.deleteMessage, name="deleteMessage"),
]

