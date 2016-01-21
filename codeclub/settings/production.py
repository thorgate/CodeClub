from settings.staging import *


ALLOWED_HOSTS = ['TODO.com']

# Static site url, used when we need absolute url but lack request object, e.g. in email sending.
SITE_URL = 'http://TODO.com'

EMAIL_HOST_PASSWORD = 'TODO (api key)'

RAVEN_CONFIG['dsn'] = 'https://TODO@sentry.thorgate.eu/TODO',
