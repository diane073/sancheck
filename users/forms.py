from django import forms
from .models import CustomUser


class SignupForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="비밀번호",
        required=True,
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="비밀번호 확인",
        required=True,
    )
    is_pet_host = forms.BooleanField(
        widget=forms.CheckboxInput(),
        label="반려동물이 있나요?",
        required=False,
    )

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "password1",
            "password2",
            "nickname",
            "email",
            "address",
            "is_pet_host",
            "pet_kind",
        )
        labels = {
            "username": "아이디",
            "nickname": "닉네임",
            "email": "이메일",
            "address": "주소",
            "pet_kind": "어떤 반려동물을 기르나요?",
        }
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "nickname": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "pet_kind": forms.Select(
                attrs={"class": "form-control"},
            ),
        }

    # ↓ clean 함수는 form이 submit 됐을 때 각 field가 가진 validator를 사용하여 입력값이 유효한지 확인
    # 비밀번호 일치 여부를 확인하는 과정을 추가하기 위해 오버라이팅
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        try:
            if password1 != password2:
                raise forms.ValidationError(
                    {
                        "password2": ["비밀번호가 일치하지 않습니다"],
                    }
                )
        except forms.ValidationError as e:
            print(f"Password Validation Error\n: {e}")
