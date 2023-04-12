from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import CommentModel
from django.http import HttpResponse

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


def comment_post(request):
    if request.method == "POST":
        # 코멘트 쓰기, 업로드
        # 업로드시 자신이 쓴 내역 가져오기
        write_comments = CommentModel(request.POST)

        if not CommentModel.content:
            # 댓글 내용이 없을 경우
            # 여기도 경로 확인해야함
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
