from django.http import HttpRequest
from rest_framework.response import Response
from datetime import datetime, timedelta
import os


class CSCookie:
    def __init__(self, request=None, response=None) -> None:
        self.response: Response = response
        self.request: HttpRequest = request
        self.__default = {
            "path": str("/"),
            "secure": bool(int(os.environ.get("SESSION_COOKIE_SAMESITE"))),
            "samesite": os.environ.get("SESSION_COOKIE_SAMESITE"),
        }

    def set(self, key: str, value: str | int, **kwargs) -> None:
        payload = {**self.__default, "key": key, "value": value, **kwargs}
        self.response.set_cookie(**payload)

    def get(self, key=str):
        cookie = self.request.COOKIES.get(key)
        return cookie

    def delete(self, key: str):
        self.response.delete_cookie(key)
