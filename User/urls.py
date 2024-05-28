
from django.contrib import admin
from django.urls import path
from .views import SignUpView
from django.contrib.auth.views import LoginView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
]
