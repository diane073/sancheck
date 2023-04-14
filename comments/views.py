from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import CommentModel
from .forms import CommentForm
from django.http import HttpResponse
from posts.models import PostModel
from django.views import generic


def comment_view(request):
    if request.method == "GET":
        # 게시글 내용이 뜰때 같이 가져옴
        all_comments = CommentModel()
        if not all_comments:
            message = "아직 댓글이 없습니다."
            return {"error_message": message}
        elif all_comments:
            return render(
                request, "/post/<int:post_id>/detail", {"all_comments": all_comments}
            )
    else:
        raise NotImplementedError()


@login_required
@csrf_exempt
def comment_post(request, post_id):
    if request.method == "POST":
        # 코멘트 쓰기, 업로드
        post = get_object_or_404(PostModel, id=post_id)
        comment_form = CommentForm(request.POST)
        content = request.POST.get("content")
        if not content:
            # 댓글 내용이 없을 경우
            # 가능하다면 html에 {{error_message}} 띄워주기
            message = "댓글 내용을 적어주세요"
            return render(request, "post/post_detail.html", {"error_message": message})

        elif comment_form.is_valid():
            # 해당하는 포스트, 요청 User함께 입력하여 저장
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            return redirect(f"/post/{post_id}/detail")
    else:
        return HttpResponse("댓글 포스트에 실패하였습니다")


@csrf_exempt
@login_required
def comment_delete(request, comment_id):
    comment = CommentModel.objects.get(id=comment_id)
    if comment.author == request.user:
        comment.delete()

    return redirect("/")


class MyCommentList(generic.ListView):
    # ListView를 사용해 댓글 10개씩 보여주기
    model = CommentModel
    template_name = "comments/my_comment.html"
    context_object_name = "latest_comment_list"
    paginate_by = 10

    def get_queryset(self):
        # 최근 댓글 불러오기
        my_comment = CommentModel.objects.all().order_by("-created_at")
        return my_comment


get_my_comments = MyCommentList
