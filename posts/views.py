import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import PostModel
from .forms import PostForm


def home(request):
    posts = PostModel.objects.all().order_by("-created_at")
    page = request.GET.get("page")
    max_post = 2  # 페이지 1개당 생성될 포스트 개수
    paginator = Paginator(posts, max_post)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:  # 페이지가 들어오지 않았다면 1페이지로 호출
        page = 1
        page_obj = paginator.page(page)
    except EmptyPage:  # 존재하지 않는 페이지 호출 방지
        page = paginator.num_pages
        page_obj = paginator.page(page)

    left_index = int(page) - 2  # 현제 페이지에서 좌우로 2칸만 출력
    if left_index < 1:  # 최소 페이지는 1페이지로 에러방지.
        left_index = 1
    right_index = int(page) + 2
    if right_index > paginator.num_pages:  # 페이지 끝이 넘어가려하면 최대 인덱스 조정
        right_index = paginator.num_pages
    custom_range = range(left_index, right_index + 1)

    return render(
        request,
        "home.html",
        {"posts": posts, "page_obj": page_obj, "custom_range": custom_range},
    )


@login_required
def post_view(request):
    if request.method == "GET":
        form = PostForm()
        return render(request, "posts/post_create.html", {"form": form})

    elif request.method == "POST":
        post_upload = PostForm(request.POST, request.FILES)
        if post_upload.is_valid():
            new_post = PostModel()
            new_post.author = request.user
            new_post.name = post_upload.cleaned_data["name"]
            new_post.description = post_upload.cleaned_data["description"]
            new_post.img_path = post_upload.cleaned_data["img_path"]
            new_post.save()
            return redirect("/")

    return redirect("/user/login")


@login_required
def post_update(request, id):
    post = get_object_or_404(PostModel, id=id)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)  # ✅
        if form.is_valid():
            PostModel.objects.filter(id=id).update(
                name=form.cleaned_data["name"],
                description=form.cleaned_data["description"],
                img_path=request.FILES.get("img_path", post.img_path),
                updated_at=datetime.datetime.now(),
            )
            return redirect("/post/" + str(id))
    else:
        form = PostForm(instance=post)  # ✅
    return render(request, "posts/post_create.html", {"form": form, "id": id})


def post_delete(request, id):
    post = PostModel.objects.get(id=id)
    post.delete()
    return redirect("/")


def post_detail(request, id):
    post = PostModel.objects.get(id=id)
    return render(request, "posts/post_detail.html", {"post": post})
