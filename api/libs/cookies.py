from rest_framework.response import Response
from datetime import datetime, timedelta


class CSCookie:
    __default = {
        "key": str,
        "value": str,
        "max_age": int | float,
        "expires": datetime.now() + timedelta(minutes=1),
        "domain": str(),
        "path": str("/"),
        "secure": bool(False),
        "samesite": "None" | "Strick" | "Lax",
        "httponly": bool(False),
    }

    @classmethod
    def set(cls, response, data=__default):

        response.set
