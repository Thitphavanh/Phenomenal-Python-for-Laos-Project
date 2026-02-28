
from django.urls import path
from . import views



app_name = 'blog'

from .feeds import LatestPostsFeed

urlpatterns = [
    # Home feed / posts
    path("", views.index, name="index"),
    path("posts/", views.post_list, name="post_list"),
    path("feed/", LatestPostsFeed(), name="post_feed"),

    # Post URLs
    path("post/<slug:slug>/", views.post_detail, name="post_detail"),
    path("create/", views.create_post, name="create_post"),
    path("post/<slug:slug>/edit/", views.edit_post, name="edit_post"),
    path("category/<slug:slug>/", views.category_posts, name="category_posts"),

    # Voting
    path("vote/<int:post_id>/", views.vote_post, name="vote_post"),

    # Authentication
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # LINE LIFF Authentication
    path("line-auth/", views.line_auth_view, name="line_auth"),
]
