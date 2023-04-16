from django.test import TestCase

"""
from django.test.utils import setup_test_environment
from django.test import Client
from django.urls import reverse

setup_test_environment()
client = Client()
"""
from django.shortcuts import render, get_object_or_404
from .models import CommentModel
from .forms import CommentForm


from django.urls import reverse
from datetime import datetime
from django.utils import timezone


def create_commnet(comment_content, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return CommentModel.objects.create(comment_content=comment_content, pub_date=time)


class TestCommentupload(TestCase):
    def test_get(self):
        response = self.client.get(reverse("comments:my_comments"))
        self.assertEqual(response.status_code, 200)


# def post_update(request, post_id):
#     post = get_object_or_404(PostModel, id=post_id)
#     if request.method == "POST":
#         form = PostForm(request.POST, request.FILES, instance=post)  # ✅

#         if form.is_valid():
#             PostModel.objects.filter(id=post_id).update(
#                 title=form.cleaned_data["title"],
#                 description=form.cleaned_data["description"],
#                 category=form.cleaned_data["category"],
#                 time=form.cleaned_data["time"],
#                 pets=form.cleaned_data["pets"],
#                 img_path=request.FILES.get("img_path", post.img_path),
#                 updated_at=datetime.datetime.now(),
#             )

#             return redirect(f"/post/" + str(post_id) + "/detail")
# ㅇ
#     else:
#         form = PostForm(instance=post)  # ✅

#     return render(request, "posts/post_create.html", {"form": form, "id": post_id})
