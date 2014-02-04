import os

import dj_database_url


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'exams',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'prereg.urls'

WSGI_APPLICATION = 'prereg.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(),
}

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'

USE_I18N = False
USE_L10N = False
USE_TZ = True

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'
