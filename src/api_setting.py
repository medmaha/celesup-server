import os
from datetime import timedelta, datetime

DEBUG = bool(int(os.environ.get("DEBUG", 1)))

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    "content-type",
    "authorization",
    "x-csrftoken",
    "celesup-api",
    "origin",
    "cs-auth",
    "cs-auth-val",
]

if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True

else:
    specified_origins = os.environ.get("CORS_ORIGIN_WHITELIST")

    if specified_origins:
        origins = specified_origins
        allowed_origins = lambda: [h.strip() for h in origins.split(",")]
        CORS_ORIGIN_WHITELIST = allowed_origins()

    else:
        CORS_ALLOW_ALL_ORIGINS = True

REST_FRAMEWORK = {
    "PAGE_SIZE": 10,
    "DEFAULT_PAGINATION_CLASS": "src.features.paginator.CelesupPaginator",
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "src.features.authenticator.CelesupAuthentication",
    ),
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ],
}

SIMPLE_JWT = {
    # "ACCESS_TOKEN_LIFETIME": timedelta(seconds=10),
    # "REFRESH_TOKEN_LIFETIME": timedelta(seconds=30),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "AUTH_HEADER_TYPES": ("Celesup", "JWT"),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "token_id",
    "SIGNING_KEY": os.getenv("CELESUP_SECRET_KEY"),
}
