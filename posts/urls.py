# tweet/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("post/note", views.post_view, name="post_view"),
    path("post/delete/<int:id>", views.post_delete, name="post_delete"),
    path("post/<int:id>", views.post_detail, name="post_detail"),
    path("post/update/<int:id>", views.post_update, name="post_update"),
]
