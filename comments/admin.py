from django.contrib import admin
from .models import CommentModel
from .forms import CommentForm

admin.site.register(CommentModel, CommentForm)


def my_comment_view(request, page=1):
    if request.method == "GET":
        cmt_amount = 10
        start_cmt = (page - 1) * cmt_amount
        end_cmt = start_cmt + cmt_amount

        comment_title = "내 댓글 목록"

        # 내 댓글 불러오기, author정보기반
        author = CommentModel.author
        my_comment = CommentModel.objects.all(author=author)[
            start_cmt:end_cmt
        ].order_by("-created")

        # return HttpResponse ('[%s]' % commnet_title)
        return render("/comment/my")
