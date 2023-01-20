from django.urls import path
from . import ProfileView, ProfileEdit, ProfileFollow, ProfileList, AuthenticateUser

from .account import AccountSettings


from .user_info import UserInformation

_users_url_patterns = [
    path('user/<str:id>', UserInformation.as_view())
]


users_url_patterns = [
    path("authenticate", AuthenticateUser.as_view()),
    path("profile/all", ProfileList.as_view()),
    path("profile/view", ProfileView.as_view()),
    path("profile/edit", ProfileEdit.as_view()),
    path("profile/follow", ProfileFollow.as_view()),
    #
    path("profile/account", AccountSettings.as_view()),
]
