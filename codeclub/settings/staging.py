from settings.base import *


DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['TODO.com']

# Static site url, used when we need absolute url but lack request object, e.g. in email sending.
SITE_URL = 'http://TODO.com'

EMAIL_HOST_PASSWORD = 'TODO (api key)'


STATIC_URL = '/assets/'

# Production logging - all INFO and higher messages go to info.log file. ERROR and higher messages additionally go to
#  error.log file plus to Sentry.
LOGGING['handlers'] = {
    'info_log': {
        'level': 'INFO',
        'class': 'logging.handlers.WatchedFileHandler',
        'filename': '/var/log/codeclub/info.log',
        'formatter': 'default',
    },
    'error_log': {
        'level': 'ERROR',
        'class': 'logging.handlers.WatchedFileHandler',
        'filename': '/var/log/codeclub/error.log',
        'formatter': 'default',
    },
    'sentry': {
        'level': 'ERROR',
        'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
    },
}
LOGGING['loggers'][''] = {
    'handlers': ['info_log', 'error_log', 'sentry'],
    'level': 'INFO',
    'filters': ['require_debug_false'],
}
# Sentry error logging
INSTALLED_APPS += (
    'raven.contrib.django.raven_compat',
)
RAVEN_CONFIG = {
    'dsn': 'https://TODO@sentry.thorgate.eu/TODO',
}
