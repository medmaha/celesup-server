import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

AUTH_USER_MODEL = "users.User"

SECRET_KEY = os.getenv("CELESUP_SECRET_KEY", os.getenv("SECRET_KEY"))

DEBUG = bool(int(os.getenv("DEBUG")))

if not DEBUG:
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(",")
else:
    ALLOWED_HOSTS = ["*"]


# Application definition
INSTALLED_APPS = [
    # "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third parties apps
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    # customs apps
    # "fake_objects.apps.FakeObjectsConfig",
    "users.apps.UsersConfig",
    "admin_users.apps.AdminUserConfig",
    "celebrity.apps.CelebrityConfig",
    "supporter.apps.SupporterConfig",
    "feed.apps.FeedConfig",
    "post.apps.PostConfig",
    "hashtags.apps.HashtagsConfig",
    "features.apps.FeaturesConfig",
    "notification.apps.NotificationConfig",
    "comment.apps.CommentConfig",
    "messenging.apps.MessengingConfig",
    # dynamic website
    # 'website.apps.WebsiteConfig',
]


MIDDLEWARE = [
    # custom Django cors headers
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "src.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "api/templates",
            BASE_DIR / "build",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "utilities.processors.profile",
            ],
        },
    },
]

WSGI_APPLICATION = "src.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "DATABASE.db",
        "OPTIONS": {
            "timeout": 20,
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "GMT"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, '"staticfiles"')

# ? DEPLOYMENT
# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, "static"),
#     os.path.join(BASE_DIR, "build/static"),
#     os.path.join(BASE_DIR, "build"),
# )


MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "MEDIA_FILES/"

# Emailing
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_USE_TLS = int(os.getenv("EMAIL_USE_TLS"))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

from .api_setting import *
