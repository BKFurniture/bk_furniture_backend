"""
Django settings for bk_furniture project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from datetime import timedelta
from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = "django-insecure--6r)hlk3mwj7^ckcr$(#*k^v+g&u!7s-+sojyt#$)g2+g)3292"
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "django-insecure--6r)hlk3mwj7^ckcr$(#*k^v+g&u!7s-+sojyt#$)g2+g)3292")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DJANGO_DEBUG", "") != "False"
# DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "django_jsonform",  # to handle ArrayField widget
    "phonenumber_field",  # to handle phone number field
    "rest_framework_simplejwt.token_blacklist",
    "users",
    "products",
    "orders",
    "ratings",
    "chatbot",
    "promotions",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = "bk_furniture.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "bk_furniture.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "BK_Furniture",
#         "USER": "postgres",
#         "PASSWORD": "123456",
#         "HOST": "127.0.0.1",
#         "PORT": "5432",
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD': 'vKeCnsQEat1xxneTNTSO',
        'HOST': 'containers-us-west-202.railway.app',
        'PORT': '7598',
    }
}

# Update database configuration from $DATABASE_URL.
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES["default"].update(db_from_env)


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# The absolute path to the directory where collectstatic will collect static files for deployment.
STATIC_ROOT = BASE_DIR / "staticfiles"

# The URL to use when referring to static files (where they will be served from)
STATIC_URL = "/static/"

# Simplified static file serving.
# https://pypi.org/project/whitenoise/
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DEFAULT_FILE_STORAGE = 'storages.backends.dropbox.DropBoxStorage'
DROPBOX_APP_KEY = os.environ.get("DROPBOX_APP_KEY") if DEBUG is False else os.getenv("DROPBOX_APP_KEY")
DROPBOX_APP_SECRET = os.environ.get("DROPBOX_APP_SECRET") if DEBUG is False else os.getenv("DROPBOX_APP_SECRET")
DROPBOX_OAUTH2_REFRESH_TOKEN = os.environ.get("DROPBOX_OAUTH2_REFRESH_TOKEN") if DEBUG is False else os.getenv("DROPBOX_OAUTH2_REFRESH_TOKEN")
# DROPBOX_OAUTH2_TOKEN = 'sl.Bcp8JS8etpoiGls81hPio92KgWhmqe1kjrhRL_aGqiumzsMHWj2HR5EMiFzItBaknNtYMbhDiWCZ0_9InkdOSXFFDsGqR3QEBntGw2ITRFv9jHrX4Znvjab3Aqw013I0vOl3QsOm'

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=10),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

# For example, for a site URL at 'web-production-3640.up.railway.app'
# (replace the string below with your own site URL):
ALLOWED_HOSTS = ['bkfurniturebackend-production.up.railway.app', '127.0.0.1', 'localhost', "enchanted-bike-production.up.railway.app"]

# For example, for a site URL is at 'web-production-3640.up.railway.app'
# (replace the string below with your own site URL):
CSRF_TRUSTED_ORIGINS = ['https://bkfurniturebackend-production.up.railway.app', 'https://enchanted-bike-production.up.railway.app']

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'https://bk-furniture-frontend.vercel.app',
]

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "access-control-allow-origin",
]

# GOOGLE AUTHENTICATION
GOOGLE_CLIENT_ID = "286394655273-rs58iifdmnkpgkerd4872fjs9mog27dv.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = None

# FACEBOOK AUTHENTICATION
FACEBOOK_APP_ID = '236109032265868'
FACEBOOK_APP_SECRET = '8da9920fd07c219d4b09a42f08f37e07'
FACEBOOK_DEBUG_TOKEN_URL = "https://graph.facebook.com/debug_token"
FACEBOOK_ACCESS_TOKEN_URL = "https://graph.facebook.com/v7.0/oauth/access_token"
FACEBOOK_URL = "https://graph.facebook.com/"

OPENAI_API_KEY = "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"
