from django.urls import path
from . import views

urlpatterns = [
    path("user/signup", views.signup_view, name="signup"),
    path("user/login", views.login_view, name="login"),
]
