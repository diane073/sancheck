from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import CommentModel

# Create your views here.
# /post/<int:_id>/detail < 글 상세보기 경로


@login_required
@csrf_exempt
def comment_view(request):
    if request.method == "GET":
        # 게시글 내용이 뜰때 같이 가져옴``
        # 여기 경로 이름 확인해야함
        all_comments = CommentModel()
        return render(request, "/post/<int:_id>/detail", {"comments": all_comments})
    else:
        raise NotImplementedError()


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


#
# comment 보여주는것은 post detail에 가져다 붙이고 따로 만들어야할지 고민..


def comment_delete_post(request):
    comment = CommentModel.objects.get(id=id)
    comment.delete
    return redirect("/post/<int:_id>/detail")
