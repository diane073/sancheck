from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import CommentModel
from .forms import CommentForm
from django.http import HttpResponse
from django.core.paginator import Paginator
from posts.models import PostModel

# Create your views here.
# /post/<int:post_id>/detail < 글 상세보기 경로


def comment_view(request):
    if request.method == "GET":  # -> posts쪽에 병합하는것으로
        # 게시글 내용이 뜰때 같이 가져옴
        # 여기 경로 이름 확인해야함
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
            # commnet/note의 html에 해당하는 것 넣어주기

        elif comment_form.is_valid():
            # 해당하는 포스트, 요청 User함께 입력하여 저장
            # comment = CommentModel()
            # comment.post = post
            # comment.author = request.user
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            return redirect(f"/post/{post_id}/detail")
    else:
        return HttpResponse("댓글 포스트에 실패하였습니다")


@csrf_exempt
@login_required
def comment_delete(request, post_id, comment_id):
    # comment_id가 일치하는 것을 가져와서 지우기
    # post_id를 가져와 지운 창에 돌아가게 해준다.
    if request.method == "POST":
        comment = CommentModel.objects.get(id=comment_id)
        comment.delete()
        return redirect(f"/post/{post_id}/detail")


def my_comment_view(request):
    if request.method == "GET":
        # 내 댓글 불러오기, author정보기반

        my_comment = CommentModel.objects.filter(author=request.user).order_by(
            "-created_at"
        )

        comment_title = "내 댓글 목록"

        paginator = Paginator(my_comment, 10)
        page = request.GET.get("page")
        print(page)
        page_obj = paginator.page(page)
        # return HttpResponse ('[%s]' % commnet_title)
        return render(
            None,
            "comments/my_comment.html",
            {"my_comment": my_comment, "page_obj": page_obj},
        )
