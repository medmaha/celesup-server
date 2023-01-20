app_name = "api"

from django.urls import path

from .routes.authentication.register import (
    Registration,
)

from .routes.authentication.login import (
    AuthenticationTokens,
    RefreshAuthenticationTokens,
)

from .routes.authentication.logout import LogoutAuthenticationTokens

from .routes.authentication.verification import VerifyEmailAddress


from .routes.dashboard.posts import posts_url_patterns
from .routes.dashboard.feed import feed_url_urlpatterns
from .routes.user import users_url_patterns
from .routes.query import query_url_patterns
from .routes.notification.urls import notifications_url_patterns
from .routes.comment.urls import comment_url_patterns
from .routes.messenging.urls import messenging_url_patterns

from django.views.generic import TemplateView

urlpatterns = [
    # registration
    # path("", TemplateView.as_view(template_name="index.html")),
    path("signup", Registration.as_view()),
    path("verify/email", VerifyEmailAddress.as_view()),
    # path("signup/user/informations", SignupUserInformation.as_view()),
    # authentication
    path("obtain/user/tokens", AuthenticationTokens.as_view()),
    path("refresh/user/tokens", RefreshAuthenticationTokens.as_view()),
    path("logout/user/tokens", LogoutAuthenticationTokens.as_view()),
    # re_path(r'', TemplateView.as_view(template_name='index.html')),
]

# api routes urls
urlpatterns += posts_url_patterns
urlpatterns += comment_url_patterns
urlpatterns += users_url_patterns
urlpatterns += query_url_patterns
urlpatterns += notifications_url_patterns
urlpatterns += messenging_url_patterns
urlpatterns += feed_url_urlpatterns
