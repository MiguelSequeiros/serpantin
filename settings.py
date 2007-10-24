# Django settings for serpantin project.

import os

users = {
    'ds': {
        'login':	'ds',
        'name':		'Dmitry Sorokin',
        'email':	'dimas@dial.com.ru', 
        'djangodir':	'/home/ds/svn/django/django', 
        'projectdir':	'/home/ds/svn/serpantin', 
    },
    'greg': { 
        'login':	'greg',
        'name':		'Grigory Fateev',
        'email':	'greg@dial.com.ru', 
        'djangodir':	'/home/greg/www/django_src/django', 
        'projectdir':	'/home/greg/www/serp2', 
    },
    'subzero': { 
        'login':	'subzero',
        'name':		'Artem Opanchuk',
        'email':	'subzero@dial.com.ru', 
        'djangodir':	'/home/subzero/svn/django-trunk/django', 
        'projectdir':	'/home/subzero/svn/serpantin', 
    },
}


user = users[os.environ['USER']]


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Dmitry Sorokin', 'dimas@dial.com.ru'),
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'postgresql' # 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = 'serpantin'             # Or path to database file if using sqlite3.
DATABASE_USER = os.environ['USER']             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/current/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
TIME_ZONE = 'Europe/Moscow'
#TIME_ZONE = 'Europe/Moscow W-SU'
#TIME_ZONE = 'Etc/GMT+3'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'ru'

DEFAULT_CHARSET = 'utf-8'

SITE_ID = 1

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/var/www/html/media/'

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = 'http://localhost/media'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'c6_+l+^%dw7@eqb&mzlc)xv18j9jsudl+=7_tm4z_76&8qvgd2'

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
    user['projectdir'] + '/templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.databrowse',
    'serpantin.apps.common',
    'serpantin.apps.test',
)



JS_URL = '/site_media/js/'

AUTH_PROFILE_MODULE = 'common.UserProfile'

