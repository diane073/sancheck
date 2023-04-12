from django.urls import path
from . import views

urlpatterns = [
    path("/comment/note", views.comment_view, name="write_comments"),
    path("/comment/my", views.my_comment_view, name="my_comments"),
]
