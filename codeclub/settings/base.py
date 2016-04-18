"""
Django settings for CodeClub project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import os

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# Build paths inside the project like this: os.path.join(SITE_ROOT, ...)
SITE_ROOT = os.path.dirname(os.path.dirname(__file__))


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

SITE_ID = 1

ADMINS = (
    ('Thorgate admins', 'errors@thorgate.eu'),
)
MANAGERS = ADMINS
EMAIL_SUBJECT_PREFIX = '[CodeClub] '  # subject prefix for managers & admins

SESSION_COOKIE_NAME = 'codeclub_ssid'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',

    'crispy_forms',
    'compressor',

    'accounts',
    'challenges',
    'codeclub',
]


MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]


TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'codeclub.context_processors.google_analytics',
]
TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]
TEMPLATE_DIRS = [
    os.path.join(SITE_ROOT, 'templates'),
]


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(SITE_ROOT, 'db.sqlite3'),
    }
}


# Caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_PREFIX': 'codeclub',
    }
}


# Internationalization
LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', 'English'),
    ('et', 'Eesti keel'),
)
LOCALE_PATHS = (
    'locale',
)

TIME_ZONE = 'Europe/Tallinn'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files and media (CSS, JavaScript, images)
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(SITE_ROOT, 'assets')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(SITE_ROOT, 'static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'tg_utils.yuglify.YuglifyCssFilter',
]
COMPRESS_JS_FILTERS = [
    'tg_utils.yuglify.YuglifyJsFilter',
]


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dummy key'

AUTH_USER_MODEL = 'accounts.User'

ALLOWED_HOSTS = []

# Static site url, used when we need absolute url but lack request object, e.g. in email sending.
SITE_URL = 'http://127.0.0.1:8000'

# Don't allow site's content to be included in frames/iframes.
X_FRAME_OPTIONS = 'DENY'


ROOT_URLCONF = 'codeclub.urls'

WSGI_APPLICATION = 'codeclub.wsgi.application'


LOGIN_REDIRECT_URL = '/'
LOGIN_URL = 'login'


# Crispy-forms
CRISPY_TEMPLATE_PACK = 'bootstrap3'


# Email config
DEFAULT_FROM_EMAIL = "CodeClub <info@TODO.com>"
SERVER_EMAIL = "CodeClub server <server@TODO.com>"

# SMTP
EMAIL_HOST = 'smtp.sparkpostmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'info@TODO.com'
EMAIL_HOST_PASSWORD = 'TODO (test api key)'


# Base logging config. Logs INFO and higher-level messages to console. Production-specific additions are in
#  production.py.
#  Notably we modify existing Django loggers to propagate and delegate their logging to the root handler, so that we
#  only have to configure the root handler.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'default': {
            'format': '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d %(funcName)s - %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'django': {'handlers': [], 'propagate': True},
        'django.request': {'handlers': [], 'propagate': True},
        'django.security': {'handlers': [], 'propagate': True},
    }
}

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Disable a few system checks. Careful with these, only silence what your really really don't need.
# TODO: check if this is right for your project.
SILENCED_SYSTEM_CHECKS = [
    'security.W001',  # we don't use SecurityMiddleware since security is better applied in nginx config
]

GOOGLE_ANALYTICS_PROPERTY_ID = None
