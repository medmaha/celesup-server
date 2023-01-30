app_name = "api"

from django.urls import path


from .routes.authentication.urls import auth_urls_patterns
from .routes.posts import posts_url_patterns
from .routes.feed import feed_url_urlpatterns
from .routes.user import users_url_patterns
from .routes.query import query_url_patterns
from .routes.notification.urls import notifications_url_patterns
from .routes.comment.urls import comment_url_patterns
from .routes.messenging.urls import messenging_url_patterns


from .routes.test_api import test_api

urlpatterns = [
    path("test", test_api),
]

# api routes urls
urlpatterns += auth_urls_patterns
urlpatterns += posts_url_patterns
urlpatterns += comment_url_patterns
urlpatterns += users_url_patterns
urlpatterns += query_url_patterns
urlpatterns += notifications_url_patterns
urlpatterns += messenging_url_patterns
urlpatterns += feed_url_urlpatterns
