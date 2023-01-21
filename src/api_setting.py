import os
from datetime import timedelta, datetime

import os

DEBUG = bool(int(os.environ.get('DEBUG')))
 

expiration_days = datetime.now() + timedelta(days=1)
expiration_time = expiration_days - datetime.now()


SESSION_COOKIE_NAME = 'cs-sessionkey'
SESSION_COOKIE_AGE = int(expiration_time.total_seconds())
SESSION_COOKIE_SECURE = bool(int(os.environ.get('SESSION_COOKIE_SECURE')))
SESSION_COOKIE_SAMESITE = os.environ.get('SESSION_COOKIE_SAMESITE')

CSRF_COOKIE_NAME = 'cs-csrfkey'
CSRF_COOKIE_AGE = SESSION_COOKIE_AGE
CSRF_COOKIE_SECURE = SESSION_COOKIE_SECURE
CSRF_COOKIE_SAMESITE = SESSION_COOKIE_SAMESITE

if DEBUG:
    # CORS_ALLOW_HEADERS ='*'
    CORS_ALLOW_ALL_ORIGINS = True

else:
    CORS_ORIGIN_WHITELIST = [
        *os.environ.get('CORS_ORIGIN_WHITELIST').split(',')
    ]
    # CORS_ALLOW_HEADERS = [
    #     'content-type',
    #     'authorization',
    #     'x-csrftoken',
    #     'celesup-api',
    # ]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    'content-type',
    'authorization',
    'x-csrftoken',
    'celesup-api',
]


REST_FRAMEWORK = {
    "PAGE_SIZE": 10,
    "DEFAULT_PAGINATION_CLASS": "api.features.paginator.CelesupPaginator",
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        'api.features.authenticator.CelesupAuthentication',
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
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "AUTH_HEADER_TYPES": ("Celesup", "JWT"),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "token_id",
    "SIGNING_KEY": os.getenv("CELESUP_SECRET_KEY", os.getenv("SECRET_KEY")),
}
