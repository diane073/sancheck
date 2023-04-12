from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .forms import SignupForm

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
            return redirect("/user/signup")

    form = SignupForm()
    return render(request, "users/signup.html", {"form": form})


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
