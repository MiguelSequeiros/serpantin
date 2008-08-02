# Django settings for serpantin project.
from local_settings import *

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
#    "diallib.context.extra_name_processor"
)

#CACHE_BACKEND = 'simple:///'
#CACHE_MIDDLEWARE_SECONDS = 600

MIDDLEWARE_CLASSES = (
#    "django.middleware.cache.CacheMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.doc.XViewMiddleware",
#    "django.middleware.transaction.TransactionMiddleware",
#    "diallib.middleware.threadlocals.ThreadLocals",
)

#DISABLE_TRANSACTION_MANAGEMENT = True

ROOT_URLCONF = 'serpantin.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates".
    # Always use forward slashes, even on Windows.
    os.path.join(PROJECT_DIR, 'templates/'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.databrowse',
#    'tagging',
    'serpantin.apps.common',
#    'serpantin.apps.test',
)

#AUTH_PROFILE_MODULE = 'common.UserProfile'
