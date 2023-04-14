from django.test import TestCase


from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from .models import CommentModel
from .forms import CommentForm
from django.http import HttpResponse
from django.core.paginator import Paginator
from posts.models import PostModel

# Create your tests here.


class TestCommentupload(TestCase):
    def comment_post(request, post_id):
        if request.method == "POST":
            # 코멘트 쓰기, 업로드
            post = get_object_or_404(PostModel, id=post_id)
            comment_form = CommentForm(request.POST)

            if not comment_form.content:
                # 댓글 내용이 없을 경우
                # 가능하다면 html에 {{error_message}} 띄워주기
                message = "댓글 내용을 적어주세요"
                return render(
                    request, "post/post_detail.html", {"error_message": message}
                )
                # commnet/note의 html에 해당하는 것 넣어주기

            elif comment_form.is_valid():
                # 해당하는 포스트, 요청 User함께 입력하여 저장
                comment = comment_form.save()
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect("/post/<int:post_id>/detail", post.post_id)
        else:
            return HttpResponse("댓글 포스트에 실패하였습니다")

    def comment_delete(request, post_id, comment_id):
        # comment_id가 일치하는 것을 가져와서 지우기
        # post_id를 가져와 지운 창에 돌아가게 해준다.
        comment = CommentModel.objects.get(id=comment_id)
        comment.delete(request)
        return redirect("/post/<int:post_id>/detail", id=post_id)

    def my_comment_view(request, page=1):
        if request.method == "GET":
            # 내 댓글 불러오기, author정보기반
            author = CommentModel.author
            comment = CommentModel()
            # my_comment = CommentModel.objects.all(author=author).order_by("-created")
            my_comment = author.comment_set.all().order_by("-created")

            comment_title = "내 댓글 목록"

            paginator = Paginator(my_comment, 10)
            page = request.GET.get("page")
            page_obj = paginator.page(page)

            # return HttpResponse ('[%s]' % commnet_title)
            return render_to_response(
                "/comment/my", {"my_comment": my_comment, "page_obj": page_obj}
            )
