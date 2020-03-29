"""
Django settings for sutrofm project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# We salute the contributions of the previous caretakers of this great project
ADMINS = (
  ('Brandon Wilson', 'brandon.wilson@rd.io'),
  ('Rebecca Stecker', 'rebecca.stecker@rdio.com'),
  ('Emily Stumpf', 'emily.stumpf@rdio.com'),
  ('Marek Kapolka', 'marek.kapolka@rd.io'),
  ('Holly French', 'holly.french@rd.io'),
  ('Jesse Mullan', 'jesse.mullan@rd.io'),
)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0mtvx^l)%ell-*zix1u$=svxhhul$n+u!d9!s^a#0q2-o9dyyh'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'rest_framework',
    'ws4redis',
    'sutrofm',
]

AUTHENTICATION_BACKENDS = [
    'social_core.backends.spotify.SpotifyOAuth2',
    'django.contrib.auth.backends.ModelBackend'  # must be after social auth backends
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sutrofm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'views')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'sutrofm.wsgi.application'

LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'handlers': {
    'console': {
      'class': 'logging.StreamHandler',
    },
  },
  'root': {
    'handlers': ['console'],
    'level': 'DEBUG',
  },
  'loggers': {
    'django': {
      'handlers': ['console'],
      'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
      'propagate': False,
    },
  },
}


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

# Set the number of seconds each message shall persited
WS4REDIS_EXPIRE = 3600

WS4REDIS_HEARTBEAT = '--heartbeat--'

WS4REDIS_PREFIX = 'sutrofm'

WEBSOCKET_URL = '/ws/'

WS4REDIS_CONNECTION = {
  'host': 'localhost',
  'port': 6379,
  'db': 0,
  'password': None,
}

AUTH_USER_MODEL = 'sutrofm.User'

SOCIAL_AUTH_USER_MODEL = 'sutrofm.User'
SOCIAL_AUTH_SPOTIFY_KEY = os.environ.get('SPOTIFY_API_KEY', '')
SOCIAL_AUTH_SPOTIFY_SECRET = os.environ.get('SPOTIFY_API_SECRET', '')
SOCIAL_AUTH_CLEAN_USERNAME_FUNCTION = 'unidecode.unidecode'
SOCIAL_AUTH_POSTGRES_JSONFIELD = True  # needed to store custom spotify specific data
