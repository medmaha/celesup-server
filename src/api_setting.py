import os
from datetime import timedelta, datetime

import os



# CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOW_HEADERS ='*'
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'content-type',
    'authorization',
    'x-csrftoken',
    'celesup-api',
]


CORS_ORIGIN_WHITELIST = [
    "http://localhost:5000",
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



# SESSION_COOKIE_AGE = 1209600 # 2 weeks in seconds
# CSRF_COOKIE_AGE = 1209600 # 2 weeks in seconds


expiration_date = datetime.now() + timedelta(days=1)
expiration_time = expiration_date - datetime.now()


CSRF_COOKIE_NAME = 'cs-csrfkey'
SESSION_COOKIE_NAME = 'cs-sessionkey'
CSRF_COOKIE_AGE = int(expiration_time.total_seconds())
SESSION_COOKIE_AGE = int(expiration_time.total_seconds())

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


DJOSER = {
    "USER_ID_FIELD": "username",
    "LOGIN_FIELD": "email",
    "PASSWORD_RESET_CONFIRM_URL": "password-reset/?uid={uid}&tkn={token}",
    "PASSWORD_RESET_CONFIRM_RETYPE": True,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
    "PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND": True,
}
