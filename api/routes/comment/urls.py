from django.urls import path, include

from .create import PostCommentCreate

# from .replies import PostCommentReplyCreate, PostCommentReplyList
from .lists import PostCommentList

comment_url_patterns = []

url_patterns = [
    path("create", PostCommentCreate.as_view(), name="comment_create"),
    path("<str:key>", PostCommentList.as_view(), name="comments_list"),
    path("reply", PostCommentCreate.as_view(), name="comment_reply"),
    # path("replies", PostCommentReplyList.as_view(), name="replies_list"),
]

comment_url_patterns.append(path("comments/", include(url_patterns)))


# from .comment_list import PostCommentList
# from rest_framework.routers import DefaultRouter


# router = DefaultRouter()
# router.register(r"create", PostCommentCreate, "comment_create")
# router.register(r"reply", PostCommentReplyCreate, "comment_reply")
# router.register(r"<str:post_id>", PostCommentList, "comment_list")

# comment_url_patterns = [
#     path("/comment/", include(router.urls)),
# ]
