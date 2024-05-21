from django.shortcuts import render
from django.urls import path
from userauths import views
# from .views import lockout_view

app_name = "userauths"

urlpatterns = [
    path("sign-up/", views.register_view, name="sign-up"),
    path("sign-in/", views.login_view, name="sign-in"),
    path("sign-out/", views.logout_view, name="sign-out"),
    # path('lockout/', lockout_view, name='lockout'),
]