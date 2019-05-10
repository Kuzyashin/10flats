# -*- coding: utf-8 -*-
import os

DEBUG = True

ALLOWED_HOSTS = ["*"]  # must specify domain for production

SECRET_KEY = 'LKasdnj1nJN81NDbf891nJANBgfkb>Ghvahv24'

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['DB_NAME'],
            'USER': os.environ['DB_USERNAME'],
            'PASSWORD': os.environ['DB_PASSWORD'],
            'HOST': os.environ['DB_HOSTNAME'],
            'PORT': os.environ['DB_PORT'],
        }
    }

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

