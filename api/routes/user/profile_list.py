from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from users.models import User
from django.db.models import Q
from .serializers import UserDetailSerializer
from utilities.generators import get_profile_data


class ProfileList(ListAPIView):
    def get_queryset(self):

        queryset = None

        try:
            if len(self.request.get_full_path().split("?")) > 1:
                query = self.request.get_full_path().split("?")[1].split("=")[1]
                query = query.strip()

                if not query:
                    return User.objects.all()

                queryset = User.objects.filter(
                    Q(username__startswith=query)
                    | Q(username__icontains=query)
                    | Q(first_name__startswith=query)
                    | Q(first_name__icontains=query)
                    | Q(last_name__icontains=query)
                    | Q(last_name__icontains=query)
                )
            else:
                queryset = User.objects.all()
        except:
            queryset = User.objects.all()

        return queryset

    def list(self, request, *args, **kwargs):

        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserDetailSerializer(page, many=True)

            data = self.get_data(serializer)

            return self.get_paginated_response(data)

        serializer = self.get_data(serializer)
        serializer = UserDetailSerializer(queryset, many=True)
        return Response(data)

    def get_data(self, serializer):

        i = serializer.data[:]

        for idx, data in enumerate(i):
            i[idx] = get_profile_data(User.objects.get(id=data["id"]))

            data = {
                "followers": "-",
                "following": "-",
                "cover_img": "-",
                "gender": "-",
                "city": "-",
                "date_joined": "-",
                "posts": "-",
                "profile_type": "-",
            }

            for j in data:
                try:
                    del i[idx][j]
                except:
                    continue

            i[idx].update(data)

        return i
