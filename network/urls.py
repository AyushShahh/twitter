
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("user/<str:username>", views.profile, name="profile"),
    path("following", views.following, name="following"),

    # API routes
    path("create", views.create, name="create"),
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("relationship/<str:username>", views.relationship, name="relationship"),
    path("like/<int:post_id>", views.like, name="like")
]
