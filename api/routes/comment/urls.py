from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import path
from .comment_create import (
    PostCommentCreate,
)

from .comment_reply import PostCommentReplyCreate, PostCommentReplyList

from .comment_list import PostCommentList

comment_url_patterns = [
    path("comments/create", PostCommentCreate.as_view(), name="comment_create"),
    path("comments/list/<str:key>", PostCommentList.as_view(), name="comments_list"),
    path(
        "comments/<str:key>/<str:paginate>",
        PostCommentList.as_view(),
        name="comment_slice",
    ),
    path(
        "comments/reply",
        PostCommentReplyCreate.as_view(),
        name="comment_reply_create",
    ),
    path(
        "comments/replies",
        PostCommentReplyList.as_view(),
        name="comment_reply_list",
    ),
]
