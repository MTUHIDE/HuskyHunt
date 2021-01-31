import os
import environ

env = environ.Env(
    DEBUG=(bool, False)
)

# Get variables from .env
environ.Env.read_env()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Set env-specific settings
SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG')

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env('GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env('GOOGLE_OAUTH2_SECRET')

EMAIL_USE_TLS = True
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_PASSWORD')
EMAIL_PORT = env.int('EMAIL_PORT')

SHOW_COMING_SOON = env.bool('SHOW_COMING_SOON', False)

DATABASES = {
    'default': env.db('DATABASE_URL', default='sqlite:///huskydb')
}

MEDIA_ROOT = env.str('MEDIA_ROOT', os.path.join(BASE_DIR, 'uploads'))

ALLOWED_HOSTS = ['*']

LOGIN_URL = 'landing'
LOGIN_REDIRECT_URL = 'catalog'

AUTHENTICATION_BACKENDS = (
 'social_core.backends.google.GoogleOAuth2',  # for Google authentication
 'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'accountant.pipeline.verify_scope',
    'accountant.pipeline.update_user_social_data'
)

INSTALLED_APPS = [
    'user',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cron',
    'rest_framework',
    'rest_framework.authtoken',
    'accountant',
    'catalog',
    'rideSharing',
    'landing',
    'polls',
    'selling',
    'social_django',
    'profanity_check',
    'moderation',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CRON_CLASSES = [
	"rideSharing.cron.ArchiveRides",
    "rideSharing.cron.deleteOldRides",
    "catalog.cron.archiveOldItems",
    "catalog.cron.deleteOldItems"
]

ROOT_URLCONF = 'mainsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'mainsite.context_processors.export_covid_var'
            ],
        },
    },
]

WSGI_APPLICATION = 'mainsite.wsgi.application'

FIXTURE_DIRS = [
    os.path.join(BASE_DIR, 'mainsite/fixtures')
]

# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "staticfiles"),
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media Files
MEDIA_URL = '/uploads/'

# Login Redirect
LOGIN_REDIRECT_URL = 'catalog/'
LOGOUT_REDIRECT_URL = '/'

#For images uploaded for items/etc
MAX_UPLOAD_SIZE = 5242880

ALLOWED_UPLOAD_IMAGES = ('jpg', 'png', 'jpeg')
