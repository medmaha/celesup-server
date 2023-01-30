from django.http import JsonResponse
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)


@api_view()
@authentication_classes([])
@permission_classes([])
def test_api(request):
    return JsonResponse({"Celesup": "Welcome Celesup API"})
