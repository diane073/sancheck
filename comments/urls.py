from django.urls import path
from . import views

urlpatterns = [
    path("/comment/note", views.signup, name="write_comments"),
    path("/comment/my", views.signin, name="my_comments"),
]
