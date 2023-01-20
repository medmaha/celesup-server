from ..routes.user.serializers import (
    AdminSerializer,
    SupporterSerializer,
    CelebritySerializer,
    UserDetailSerializer,
)
import os

BASE_URL = os.environ.get("BASE_URL")


class Profile:
    """Combine the clients's profile and user information"""

    def __init__(self, user, **kwargs) -> None:
        self.user = user
        self.profile = user.profile
        self.kwargs = kwargs
        self.is_admin = kwargs.get("is_admin")
        self.more_info = kwargs.get("more_info")

    def get_profile_data(self):
        profile = {}
        if self.user.user_type.lower().startswith("cel"):
            profile = CelebritySerializer(self.user.profile).data

        if self.user.user_type.lower().startswith("sup"):
            profile = SupporterSerializer(self.user.profile).data

        if self.user.user_type.lower().startswith("admin"):
            serializer = AdminSerializer(self.user.profile).data
            profile = UserDetailSerializer(self.user).data
            profile["user_type"] = serializer["profile_type"]

        if self.kwargs.get("profile"):
            if hasattr(self.user.profile, "friends"):
                profile["friends"] = len(profile["friends"])

            if hasattr(self.user.profile, "following"):
                profile["following"] = len(profile["following"])

            if hasattr(self.user.profile, "followers"):
                profile["followers"] = len(profile["followers"])
            profile["user_type"] = self.profile.profile_type.capitalize()

        return profile

    def get_user_data(self):
        data = UserDetailSerializer(self.user).data
        if self.kwargs.get("profile"):
            user = {
                "gender": self.user.gender,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
                "city": self.user.city,
                "biography": self.user.biography,
                # 'data_joined': self.user.data_joined
            }
            data.update(user)

        return data

    @property
    def data(self):
        response = {}
        response.update(self.get_user_data())
        response.update(self.get_profile_data())

        # post = self.kwargs.get('post')
        # if post:
        #     response.update({'picture': BASE_URL + post.picture.url})
        return response
