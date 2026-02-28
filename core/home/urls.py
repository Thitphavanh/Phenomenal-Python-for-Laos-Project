
from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    # Home feed / posts
    path("", views.index, name="index"),
        # Authentication
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # LINE LIFF Authentication
    path("line-auth/", views.line_auth_view, name="line_auth"),
]
