"""
Django settings for tark project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from tark.settings import secrets

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(=tzgu^(%+h6g9q!e3t7ne-m_+w3i8=w#k$r2so0)tl56b##6y'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'prem-ml']

DATABASE_ROUTERS = ['tark.routers.TarkRouter']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_swagger',
    'session',
    'genome',
    'assembly',
    'sequence',
    'exon',
    'genenames',
    'gene',
    'operon',
    'release',
    'transcript',
    'translation',
    'tagset',
    'tark_drf',
    'tark_web',
    'refseq_loader',
    'fixture_magic',
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

ROOT_URLCONF = 'tark.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # custom
                'tark_web.context_processors.init_assembly_releases',
            ],
        },
    },
]

WSGI_APPLICATION = 'tark.wsgi.application'
# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

if 'TRAVIS' in os.environ:
    SECRET_KEY = "SecretKeyForUseOnTravis"
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'tark_django_manager',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
            'PORT': '3306',
        },
        'tark': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'tark_refseq_new4',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
            'PORT': '3306',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'tark_django_manager',
            'USER': secrets.DATABASE_USER,
            'PASSWORD': secrets.DATABASE_PASSWORD,
            'HOST': secrets.DATABASE_HOST,
            'PORT': secrets.DATABASE_PORT,
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
                }
        },
        'tark': {
            'ENGINE': 'django.db.backends.mysql',
            #'NAME': 'tark_refseq_new4',
            'NAME': 'tark_refseq_dryrun',
            'USER': secrets.DATABASE_USER,
            'PASSWORD': secrets.DATABASE_PASSWORD,
            'HOST': secrets.DATABASE_HOST,
            'PORT': secrets.DATABASE_PORT,
        },
        'tark_loader': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'tark_refseq_dryrun',
            'USER': secrets.DATABASE_USER,
            'PASSWORD': secrets.DATABASE_PASSWORD,
            'HOST': secrets.DATABASE_HOST,
            'PORT': secrets.DATABASE_PORT,
        }
    }


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

REST_FRAMEWORK = {
    'PAGE_SIZE': 10,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',

    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}

SWAGGER_SETTINGS = {
    "exclude_namespaces": [],  # List URL namespaces to ignore
    "api_version": '0.1',  # Specify your API's version
    "api_path": "/",  # Specify the path to your API not a root level
    "api_key": '',  # An API key
    "is_authenticated": False,  # Set to True to enforce user authentication,
    "is_superuser": False,  # Set to True to enforce admin only access
    'VALIDATOR_URL': None,
}

LOG_FILE = os.path.join(BASE_DIR, 'logs/tark.log')
print(LOG_FILE)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOG_FILE,
        },
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
     },
}


SESSION_EXPIRE_AT_BROWSER_CLOSE = True
CURRENT_ASSEMBLY = "GRCh38"
CURRENT_RELEASE = "93"
DEFAULT_SOURCE = "ensembl"
INI_FILE = os.path.join(BASE_DIR, '../refseq_loader/management/commands/refseq_source.ini')
