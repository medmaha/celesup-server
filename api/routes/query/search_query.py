from itertools import chain
import random

from django.db.models import Q
from users.models import User
from users.serializers import UserViewSerializer
from post.models import Post
from api.routes.posts.serializers import PostDetailSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from rest_framework.decorators import api_view

from api.routes.hashtags.serializer import HashTagDetailSerializer

from hashtags.models import HashTag


class Searching(GenericAPIView):
    def make_query(self):

        pass

    def post(self, request, *args, **kwargs):
        query = request.data.get("query")
        hashtags_query = []
        users_query = []

        if query == "@*.":
            users_query = UserViewSerializer(
                User.objects.filter(),
                many=True,
            ).data

        elif query and len(query) < 3:
            # hashtags_query = HashTagDetailSerializer(
            #     HashTag.objects.filter(Q(tag_text__startswith=query))[:3], many=True
            # ).data

            users_query = UserViewSerializer(
                User.objects.filter(
                    Q(username__icontains=query) | Q(name__icontains=query)
                )[:3],
                many=True,
            ).data

        elif query and (not hashtags_query or not users_query):

            query = query[: len(query) - 1]

            # hashtags_query = HashTagDetailSerializer(
            #     HashTag.objects.filter(Q(tag_text__icontains=query))[:3], many=True
            # ).data

            users_query = UserViewSerializer(
                User.objects.filter(
                    Q(username__icontains=query) | Q(name__icontains=query)
                )[:3],
                many=True,
            ).data

        elif len(query) >= 3:
            # hashtags_query = HashTagDetailSerializer(
            #     HashTag.objects.filter(Q(tag_text__icontains=query))[:3], many=True
            # ).data

            users_query = UserViewSerializer(
                User.objects.filter(
                    Q(username__icontains=query) | Q(name__icontains=query)
                )[:3],
                many=True,
            ).data

        # package = package_query(
        #     hashtags_query, lookup="tag_text", object_type="hashtag"
        # )
        package = package_query(users_query, lookup="username", object_type="user")

        package = list(package.values())
        random.shuffle(package)

        return Response(package, status=200)


def package_query(query, lookup: str, object_type: str, pk="id", items={}):

    package = {}

    for instance in query:
        package[instance[pk]] = {
            "id": instance[pk],
            "text": instance[lookup].capitalize(),
            "object": object_type,
            "name": instance.get("name"),
            "avatar": instance.get("avatar", "media/no/avatar/provided"),
        }

    package.update(items)
    return package
