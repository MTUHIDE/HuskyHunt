from .base_settings import *

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = False

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ['GOOGLE_OAUTH2_KEY']
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ['GOOGLE_OAUTH2_SECRET']

EMAIL_USE_TLS = True
EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_HOST_USER = os.environ['EMAIL_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_PASSWORD']
EMAIL_PORT = int(os.environ['EMAIL_PORT'])
