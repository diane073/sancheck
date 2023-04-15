from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from .models import CustomUser

# ✅ ↓ For Email Authentication
# from allauth.account.views import SignupView


# class AuthSignupView(SignupView):
#     app_name = "users"
#     template_name = "templates/users/signup.html"


# auth_signup_view = AuthSignupView.as_view()


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            # ↓ If "commit" is False, DB에 곧바로 저장되는 것을 막는다.
            # DB에 저장되기 전에 사용자 설정을 하고 싶을 때 주로 사용한다.
            # 여기서는 비밀번호 일치 여부를 확인한다.
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            return redirect("/user/login")
        else:
            error = "입력값이 잘못됐습니다."
            context = {"error": error, "form": form}
            return render(request, "users/signup.html", context)

    form = SignupForm()
    context = {"form": form}
    return render(request, "users/signup.html", context)


def login(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            return render(request, "users/login.html", {"error": "아이디 또는 비밀번호를 확인해주세요"})

    elif request.method == "GET":
        user = request.user.is_authenticated
        if user:
            return redirect("/")
        else:
            return render(request, "users/login.html")


@login_required
def logout(request):
    auth.logout(request)
    return redirect("/")


@login_required
def profile(request):
    if request.method == "POST":
        user = get_object_or_404(CustomUser, id=request.user.id)
        if request.POST.get("nickname"):
            user.nickname = request.POST.get("nickname")

        if request.POST.get("address"):
            user.address = request.POST.get("address")

        if request.POST.get("is_pet_host") == "true":
            user.is_pet_host = True
        else:
            user.is_pet_host = False

        user.pet_kind = request.POST.get("pet_kind")
        user.save()
        return redirect("/user/profile")
    return render(request, "users/profile.html")
