import os
# Local settings for Django projects
# Set all values here before starting the project
# Move this file to the same folder as main settings.py file
# Rename the file as local_settings.py

DEBUG = True

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ADMINS = (
    ('Seshagiri Prabhu', 'seshagiriprabhu@gmail.com'),
)

ADMINS_EMAIL = map(lambda x: x[1], ADMINS)

# Sending email using SMTP gmail server

#EMAIL_HOST_USER = 'amritapurifoss@gmail.com'
#EMAIL_HOST_PASSWORD = ''
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


# If running in debug mode, write emails to files.
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = '/tmp'

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Generate a secret key, and don't share it with anybody.
# from django.utils.crypto import get_random_string
# chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
# get_random_string(50, chars)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'k%m(0me09-zyjh32s)2oo8j*_#ivjdoa6jeqmx#(sz+06e2t#8'

#password_hashers
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)

# To be changed with site specific values
RECAPTCHA_PUBLIC_KEY = '6LfcYvkSAAAAAAW8UHVHw3oBuF7S5NJZ-jnBUxn1'
RECAPTCHA_PRIVATE_KEY = '6LfcYvkSAAAAAOkXjirru1nTiwvwi_drX93sTQKo'
RECAPTCHA_USE_SSL = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',    # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'db/db.db',                         # Or path to database file if using sqlite3.
        'USER': '',                    # Not used with sqlite3.
        'PASSWORD': '',                   # Not used with sqlite3.
        'HOST': '',                              # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                              # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Kolkata'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}