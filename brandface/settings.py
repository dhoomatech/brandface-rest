"""
Django settings for brandface project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
from .env import env
from datetime import timedelta


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = Path(__file__).resolve().parent

SITE_HOST = env.str('SITE_HOST')
SITE_URL_HTTP = 'http://{}'.format(SITE_HOST)
SITE_URL_HTTPS = 'https://{}'.format(SITE_HOST)

# USE_SSL = env.bool('USE_SSL', default=False)
# if USE_SSL:
#     DEFAULT_SITE_URL = SITE_URL_HTTPS
#     SECURE_SSL_REDIRECT = False
#     SESSION_COOKIE_SECURE=True
#     SECURE_HSTS_SECONDS = 31536000 #1 year, is common
#     SECURE_REDIRECT_EXEMPT = [r'^no-ssl/$']
#     SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
#     SECURE_PROXY_SSL_HEADER = ('HTTP_X_SCHEME', 'https')
# else:
#    DEFAULT_SITE_URL = SITE_URL_HTTP

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-=57vf463783^b_4h274&8mm(vq#4nu6p^u=jm3uh^tp%le2=j9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["13.112.86.78","127.0.0.1","api-uat.brandface.me"]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',

    'drf_spectacular',
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    # 'debug_toolbar',
    'sslserver',
    
    'core',
    'dh_user',
    'dh_content',
]

MIDDLEWARE = [
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'brandface.urls'
AUTH_USER_MODEL = 'dh_user.User'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'brandface.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASE_POSTGRESS = env.bool('DATABASE_POSTGRESS',False)

if DATABASE_POSTGRESS:
    DATABASES = {'default': env.db('DATABASE_URL')}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# For JWT
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}


# JWT settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=15),
    'SLIDING_TOKEN_LIFETIME': timedelta(days=30),
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}


# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.redis.RedisCache",
#         "LOCATION": [
#             "redis://127.0.0.1:6379",  # leader
#             # "redis://127.0.0.1:6378",  # read-replica 1
#             # "redis://127.0.0.1:6377",  # read-replica 2
#         ],
#         "KEY_PREFIX": "dh",
#         "TIMEOUT": 60 * 15,  # in seconds: 60 * 15 (15 minutes)
#     }
# }

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(os.path.dirname(BASE_DIR), 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

#Media File
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(PROJECT_DIR), 'media')
MEDIAFILES_DIRS = (
    os.path.join(BASE_DIR, 'media'),
)
# COMPRESS_ENABLED = True


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


SITE_NAME = "Brandface"
SITE_DESCRIPTION = ""

SITE_URL = ""
SITE_METAIMAGE = ""
GOOGLE_ANALYTICS_KEY = ""