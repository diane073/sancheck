import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import PostModel
from comments.models import CommentModel
from comments.forms import CommentForm
from .forms import PostForm

# Create your views here.


def pagination(page, posts):
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
    return page_obj, custom_range


def home(request):
    posts = PostModel.objects.all().order_by("-created_at")
    page = request.GET.get("page")
    page_obj, custom_range = pagination(page, posts)
    category_list = set(
        [(post.category, post.get_category_display()) for post in posts]
    )
    # category_list = PostModel.CATEGORY_CHOICES
    # 카테고리에 글이 없더라도 카테고리가 출력되게 하려면 해당 방식으로 수정이 좋을 것 같음.

    return render(
        request,
        "home.html",
        {
            "posts": posts,
            "page_obj": page_obj,
            "custom_range": custom_range,
            "category": category_list,
        },
    )


def category_view(request, category):
    posts = PostModel.objects.filter(category=category).order_by("-updated_at")
    page = request.GET.get("page")
    page_obj, custom_range = pagination(page, posts)
    return render(
        request,
        "posts/category_page.html",
        {"posts": posts, "page_obj": page_obj, "custom_range": custom_range},
    )


@login_required
def my_post_view(request):
    posts = PostModel.objects.filter(author=request.user).order_by("-updated_at")
    return render(request, "posts/my_post_page.html", {"posts": posts})


@login_required
def my_comment_view(request):
    comments = CommentModel.objects.filter(author=request.user).order_by("-updated_at")
    return render(request, "posts/my_comment_page.html", {"comments": comments})


@login_required
def post_view(
    request,
):
    if request.method == "GET":
        form = PostForm()
        return render(request, "posts/post_create.html", {"form": form})

    elif request.method == "POST":
        print(request.POST)
        post_upload = PostForm(request.POST, request.FILES)
        if post_upload.is_valid():
            new_post = PostModel()
            new_post.author = request.user
            new_post.category = post_upload.cleaned_data["category"]
            new_post.title = post_upload.cleaned_data["title"]
            new_post.time = post_upload.cleaned_data["time"]
            new_post.pets = post_upload.cleaned_data["pets"]
            new_post.description = post_upload.cleaned_data["description"]
            new_post.img_path = post_upload.cleaned_data["img_path"]
            new_post.save()
            return redirect("/")

    return redirect("/user/login")


@login_required
def post_update(request, post_id):
    post = get_object_or_404(PostModel, id=post_id)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)  # ✅

        if form.is_valid():
            PostModel.objects.filter(id=post_id).update(
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                category=form.cleaned_data["category"],
                time=form.cleaned_data["time"],
                pets=form.cleaned_data["pets"],
                img_path=request.FILES.get("img_path", post.img_path),
                updated_at=datetime.datetime.now(),
            )

            return redirect("/post/" + str(post_id) + "/detail")

    else:
        form = PostForm(instance=post)  # ✅

    return render(request, "posts/post_create.html", {"form": form, "id": post_id})


def post_delete(request, post_id):
    post = PostModel.objects.get(id=post_id)
    post.delete()
    return redirect("/")


def post_detail(request, post_id):
    form = CommentForm()
    post = PostModel.objects.get(id=post_id)
    comments = (
        CommentModel.objects.all().filter(post_id=post_id).order_by("-updated_at")
    )
    context = {"form": form, "post": post, "comments": comments}
    return render(request, "posts/post_detail.html", context)
