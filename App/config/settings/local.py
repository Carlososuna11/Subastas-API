from .base import *

DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['*']
# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': {
        'user': env.str('USER'),
        'password': env.str('PASSWORD'),
        'host': env.str('HOST',default='localhost'),
        'database': env.str('DATABASE'),
        'port': env.str('PORT',default='3306')
    }
}

DATABASE = {
        'user': env.str('USER'),
        'password': env.str('PASSWORD'),
        'host': env.str('HOST',default='localhost'),
        'database': env.str('DATABASE'),
        'port': env.str('PORT',default='3306')
    }

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'