from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .forms import SignupForm


def signup_view(request):
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
            return redirect("/user/signup")

    form = SignupForm()
    return render(request, "users/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        return redirect("/")

    # form = LoginForm()
    return render(request, "users/login.html")
