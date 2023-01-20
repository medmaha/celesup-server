from ..routes.user.serializers import UserDetailSerializer

BASE_URL = "http://localhost:8000"


class PostLikedByUsers:
    def __init__(self, post, user):
        self.post = UserDetailSerializer(post.likes.all(), many=True).data
        self.admin = post.author
        self.user = user

        for postData in self.post:
            postData["avatar"] = BASE_URL + postData["avatar"]

    def remove_admin_from_likes(self):
        for idx, user in enumerate(self.post):
            if user.get("id") == self.admin.id or user.get("id") == self.user.id:
                del self.post[idx]
        return self.post

    @property
    def data(self):
        return self.remove_admin_from_likes()[:6]
