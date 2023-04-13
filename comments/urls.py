from django.urls import path
from . import views

urlpatterns = [
    path("<int:post_id>/comment/note", views.comment_post, name="write_comments"),
    path(
        "post/<int:post_id>/comment/<int:comment_id>/delete",
        views.comment_delete,
        name="delete_comment",
    ),
    path("/comment/my", views.my_comment_view, name="my_comments"),
]
