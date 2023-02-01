from urllib import response
from django.http import HttpResponse
from django.middleware.csrf import get_token


def csrf(request):
    response = HttpResponse(status=200)
    response["X-CSRFToken"] = get_token(request)
    return response
