from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import CommentModel
from .forms import CommentForm
from django.http import HttpResponse
from posts.views import post_detail

# Create your views here.
# /post/<int:_id>/detail < 글 상세보기 경로


@login_required
@csrf_exempt
def comment_view(request):
    if request.method == "GET":  # -> posts쪽에 병합하는것으로
        # 게시글 내용이 뜰때 같이 가져옴
        # 여기 경로 이름 확인해야함
        all_comments = CommentModel()
        if not all_comments:
            message = "아직 댓글이 없습니다."
            return {"error_message": message}
        elif all_comments:
            return render(request, "/post/<int:_id>/detail", {"comments": all_comments})
    else:
        raise NotImplementedError()


def comment_post(request):
    if request.method == "POST":
        # 코멘트 쓰기, 업로드
        write_comments = CommentForm(request.POST)

        if not write_comments.content:
            # 댓글 내용이 없을 경우
            # 가능하다면 html에 {{error_message}} 띄워주기
            message = "댓글 내용을 적어주세요"
            return render(request, "/comment/note", {"error_message": message})

        elif write_comments.is_valid():
            write_comments.save()
            return redirect("/post/<int:_id>/detail")
    else:
        return HttpResponse("댓글 포스트에 실패하였습니다")


def comment_delete_post(request):
    comment = CommentModel.objects.get(id=id)
    comment.delete
    return redirect("/post/<int:_id>/detail")


def my_comment_view(request, page=1):
    if request.method == "GET":
        cmt_amount = 10
        start_cmt = (page - 1) * cmt_amount
        end_cmt = start_cmt + cmt_amount

        comment_title = "내 댓글 목록"

        # 내 댓글 불러오기, author정보기반
        author = CommentModel.author
        my_comment = CommentModel.objects.all(author=author)[
            start_cmt:end_cmt
        ].order_by("-created")

        # return HttpResponse ('[%s]' % commnet_title)
        return render("/comment/my", {"my_comment": my_comment})
