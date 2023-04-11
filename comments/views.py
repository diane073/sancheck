from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import CommentModel

# Create your views here.


@login_required
@csrf_exempt
def comment_view(request):
    if request.method == 'GET':
        #게시글 내용이 뜰때 같이 가져옴
        #여기 링크 이름 확인해야함
        all_comments = CommentModel()
        return render(request, '/post/details',{'comments': all_comments})
    elif request.method == 'POST':
        #코멘트 쓰기, 업로드
        #업로드시 자신이 쓴 내역 가져오기
        new_comments = CommentModel(request.POST)
        
        if new_comments.is_valid():
            new_comments.save()
            return redirect('/post/')

def comment_delete(request):
    