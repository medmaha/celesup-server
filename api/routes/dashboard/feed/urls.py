from django.urls import path
from .feed_list import FeedPost
from .feed_remove import FeedRemove
from .feed_not_interested import FeedNotInterested

feed_url_urlpatterns = [
    path("feeds", FeedPost.as_view()),
    path("feeds/remove", FeedRemove.as_view()),
    path("feeds/not/interested", FeedNotInterested.as_view()),
]
