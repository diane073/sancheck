from django.urls import path
from . import views

urlpatterns = [
    path("post/<int:post_id>/comment", views.comment_post, name="write_comments"),
    path(
        "post/comment/<int:comment_id>/delete",
        views.comment_delete,
        name="delete_comment",
    ),
    path("comment/my", views.get_my_comments.as_view(), name="my_comments"),
]
