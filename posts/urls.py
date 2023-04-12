# tweet/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("post/note", views.post_view, name="post_view"),
    path("post/<int:post_id>/delete", views.post_delete, name="post_delete"),
    path("post/<int:post_id>/detail", views.post_detail, name="post_detail"),
    path("post/<int:post_id>/update", views.post_update, name="post_update"),
]
