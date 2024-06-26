# coding=utf-8
"""
GeoHosting Controller.

.. note:: Project level settings.
"""
import os  # noqa

from .contrib import *  # noqa

ALLOWED_HOSTS = ['*']
ADMINS = ()
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DATABASE_NAME'],
        'USER': os.environ['DATABASE_USERNAME'],
        'PASSWORD': os.environ['DATABASE_PASSWORD'],
        'HOST': os.environ['DATABASE_HOST'],
        'PORT': 5432,
        'TEST_NAME': 'unittests',
    }
}

# Set debug to false for production
DEBUG = TEMPLATE_DEBUG = False

# Extra installed apps
INSTALLED_APPS = INSTALLED_APPS + (
    'core',
    'geohosting_controller'
)
