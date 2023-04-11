from django.urls import path
from . import views

urlpatterns = [
    path("/comment/note", views.comment_view, name="write_comments"),
    # path("/comment/my", views., name="my_comments"),
]
