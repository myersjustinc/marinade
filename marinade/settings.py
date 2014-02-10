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
    'registration',
    'prereg',
    'schedule',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'marinade.urls'

WSGI_APPLICATION = 'marinade.wsgi.application'

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

EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', '') != ''
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'localhost')
EMAIL_PORT = os.environ.get('EMAIL_PORT', 1025)
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'django@localhost')

ACCOUNT_ACTIVATION_DAYS = 7
LOGIN_REDIRECT_URL = '/'
