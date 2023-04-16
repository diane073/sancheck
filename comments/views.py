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
            return render(request, "post/post_detail.html")

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
        post_id = comment.post_id
        comment.delete()

        return redirect(f"/post/{post_id}/detail")
    else:
        return HttpResponse("댓글 주인아니면 삭제 실패")


@csrf_exempt
@login_required
def comment_update(request, comment_id):
    comment = get_object_or_404(CommentModel, id=comment_id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)

        # if form.is_valid():
        #     comment = comment.save(update_fields=["content", "updated_at"])
        #     post_id = comment.post_id
        #     return render(request, "post/post_detail.html")

        if form.is_valid():
            comment = comment.update(
                content=form.cleaned_data["content"],
                updated_at=form.cleaned_data["updated_at"],
            )
            post_id = post_id = comment.post_id
            return redirect(f"/post/{post_id}/detail")

        else:
            return HttpResponse("댓글 수정에 실패했습니다. 다시 시도해주세요")

    else:
        form = CommentForm(instance=comment)
        return render(request, "comment_update.html", {"form": form, "comment_id": comment_id})


class MyCommentList(generic.ListView):
    # ListView를 사용해 댓글 10개씩 보여주기
    model = CommentModel
    template_name = "comments/my_comment.html"
    context_object_name = "latest_comment_list"
    paginate_by = 20

    def get_queryset(self):
        # 최근 댓글 불러오기
        my_comment = CommentModel.objects.all().order_by("-created_at")
        return my_comment


get_my_comments = MyCommentList
