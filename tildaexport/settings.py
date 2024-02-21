import os
import raven
import logging
#import sentry_sdk
#from sentry_sdk.integrations.django import DjangoIntegration

#sentry_sdk.init(
#    dsn="http://89ae35d5c9a84a8397f668e6a5c848ff@sentry.lektorium.tv/7",
#    integrations=[DjangoIntegration()],
#    traces_sample_rate=1.0,
#    send_default_pii=True
#)

#logging.basicConfig(level=logging.DEBUG, format="%(name)s.%(funcName)s() l.%(lineno)s -\033[32m %(message)s \033[39m")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'lek#!vef)!az%&yvn390_z5$65(wc*op%0c24%fja!3pem6uk4$s@'

DEBUG = True

SITE_ID = 1
USE_SSL = True
#APPEND_SLASH = False

ALLOWED_HOSTS = ["tilda.lektorium.tv", 'localhost']

CORS_ORIGIN_WHITELIST = (
    'http://*.lektorium.tv',
    'http://localhost:8000',
)

CORS_ORIGIN_ALLOW_ALL = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'celery',
    'export_app',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'corsheaders',
    'raven.contrib.django.raven_compat',
    'django_celery_results',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tildaexport.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
WSGI_APPLICATION = 'tildaexport.wsgi.application'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': "tilda1",
#         'USER': 'tilda',
#         'PASSWORD': 'tildapassword',
#         'OPTIONS': {
#                 'charset': 'utf8mb4',
#             }
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'tildaexport/../db.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/projects/'

RAVEN_CONFIG = {
    'dsn': 'http://89ae35d5c9a84a8397f668e6a5c848ff:8d499d950c094019809070d5e4d4f553@sentry.lektorium.tv/7',
}

#DJANGO_LOG_LEVEL=DEBUG

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}

CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"

CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'

# celery setting.
CELERY_CACHE_BACKEND = 'default'

# django setting.
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
    }
}