from django.urls import path
from . import views

urlpatterns = [
    path("/comment/note", views.comment_post, name="write_comments"),
    # path("/comment/my", views.signin, name="my_comments"),
]
