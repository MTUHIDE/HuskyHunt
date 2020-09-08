from .base_settings import *

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = False

EMAIL_USE_TLS = True
EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_HOST_USER = os.environ['EMAIL_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_PASSWORD']
EMAIL_PORT = int(os.environ['EMAIL_PORT'])
