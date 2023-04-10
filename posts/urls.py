# tweet/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),  # 127.0.0.1:8000 과 views.py 폴더의 home 함수 연결
    path('post/note', views.post_view, name='post_view'),  # 127.0.0.1:8000/tweet 과 views.py 폴더의 tweet 함수 연결
    path('post/delete/<int:id>', views.post_delete, name='post_delete'),
    path('post/<int:id>', views.post_detail, name='post_detail'),
    path('post/update/<int:id>', views.post_update, name='post_update'),
]