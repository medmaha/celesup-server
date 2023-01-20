from rest_framework import pagination
from rest_framework.response import Response
from django.conf import settings

import math


class CelesupPaginator(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        page_count = self.page.paginator.count
        page_index = self.page.number
        page_size = settings.REST_FRAMEWORK["PAGE_SIZE"]

        return Response(
            {
                "page_size": page_size,
                "page_index": page_index,
                "pages_count": math.floor(page_count / page_size),
                "objects_count": page_count,
                "links": {
                    "next": self.get_next_link(),
                    "prev": self.get_previous_link(),
                },
                "data": data,
            }
        )
