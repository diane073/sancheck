import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import PostModel
from .forms import PostForm

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import PostModel
from .forms import PostForm

# Create your views here.


def home(request):
    posts = PostModel.objects.all().order_by("-created_at")  # 게시된 포스트 전부를 최신순으로 정렬
    return render(request, "home.html", {"posts": posts})


def post_view(request):
    if request.method == "GET":
        form = PostForm()
        return render(request, "posts/post_create.html", {"form": form})

    elif request.method == "POST":
        user = request.user.is_authenticated
        if user:
            post_upload = PostForm(request.POST, request.FILES)

            if post_upload.is_valid():
                m = PostModel()
                m.name = request.POST.get("name", "")
                m.description = request.POST.get("description", "")
                m.img_path = post_upload.cleaned_data["img_path"]
                m.save()
                return redirect("/")
        else:
            return  # 로그인페이지


@login_required
def post_update(request, id):
    post = get_object_or_404(PostModel, id=id)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            PostModel.objects.filter(id=id).update(
                name=request.POST.get("name", ""),
                description=request.POST.get("description", ""),
                img_path=request.FILES.get("img_path", post.img_path),
                updated_at=datetime.datetime.now(),
            )
            return redirect("/post/" + str(id))
    else:
        form = PostForm(instance=post)
    return render(request, "posts/post_create.html", {"form": form, "id": id})


# 유저 자신의 것만 삭제가 보이게 할것이기때문에 굳이 검증이 필요한가
def post_delete(request, id):
    post = PostModel.objects.get(id=id)
    post.delete()
    return redirect("/")


def post_detail(request, id):
    post = PostModel.objects.get(id=id)
    return render(request, "posts/post_detail.html", {"post": post})
