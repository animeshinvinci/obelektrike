"""
Django settings for obelektrike project.

Generated by 'django-admin startproject' using Django 2.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


_ul = lambda s: s # noqa

env = environ.Env()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8-dqq8fw(c9x3!xki)0&@oaxqv%b5_69ub*6r2p*=2o4d+hj(b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

ADMINS = (
    ('Vsevolod Dudakov', 'vsdudakov@gmail.com'),
    ('Valentin Poloskin', 'vvpoloskin@gmail.com'),
)


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
]

INSTALLED_APPS += [
    'ckeditor',
    'ckeditor_uploader',
    'mptt',
    'compressor',
    'sorl.thumbnail',
]

INSTALLED_APPS += [
    'apps.design',
    'apps.generic',
    'apps.email',
    'apps.users',
    'apps.cms',
    'apps.blogs',
    'apps.questions',
    'apps.advert',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

ROOT_URLCONF = 'obelektrike.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'apps.cms.context_processors.cms_context_processors',
                'apps.generic.context_processors.main_context_processors',
            ],
        },
    },
]

if DEBUG:
    TEMPLATES[0]['OPTIONS']['context_processors'] += [
        'django.template.context_processors.debug',
    ]

WSGI_APPLICATION = 'obelektrike.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': env.db('DATABASE_URL'),
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

USE_ETAGS = True

SEND_BROKEN_LINK_EMAILS = True

if DEBUG:
    USE_ETAGS = False
    SEND_BROKEN_LINK_EMAILS = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',

    'compressor.finders.CompressorFinder',
)

AUTH_USER_MODEL = 'users.User'
LOGIN_URL = '/u/login/'
LOGOUT_URL = '/u/logout/'

SITE_ID = 1

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },

    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', ],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
COMPRESS_STORAGE = 'compressor.storage.GzipCompressorFileStorage'

SUPPORT_EMAIL = "support@obelektrike.ru"
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_HOST_USER = SUPPORT_EMAIL
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 465
SERVER_EMAIL = SUPPORT_EMAIL
DEFAULT_FROM_EMAIL = SUPPORT_EMAIL


CKEDITOR_JQUERY_URL = "/static/jquery/jquery.min.js"
CKEDITOR_UPLOAD_PATH = "uploads/posts/"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            [
                'NumberedList',
                'BulletedList',
                '-',
                'Outdent',
                'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'
            ],
            ['Image'],
            ['Link', 'Unlink'],
            ['RemoveFormat', 'Source'],
            ['Advert'],
        ],
        'allowedContent': True,
        'removeFormatAttributes': '',
        # 'extraPlugins': 'adverts,',
    },
    'comment': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList']
        ],
    },
    'feedback': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList']
        ],
        'width': '100%',
        'height': 300,
    },
}


MATERIAL_TYPE_ADV = 0
MATERIAL_TYPE_RULES = 1
MATERIAL_TYPE_FEEDBACK = 3
MATERIAL_LOGIN = 4
MATERIAL_REGISTRATION = 5
MATERIAL_CHANGEPASSWORD = 6
MATERIAL_ABOUT = 7
MATERIAL_CREATE_POST = 8
MATERIAL_CREATE_QUESTION = 9
MATERIAL_NOTES = 10
MATERIAL_JOKES = 11
MATERIAL_COMMENT_POSTS = 12
MATERIAL_QUESTION_POSTS = 13
MATERIAL_NEW_POSTS = 14
MATERIAL_PRACTIC_POSTS = 15
MATERIAL_ADV_RIGHT = 16
MATERIAL_ADV_TOP = 17
MATERIAL_NEWS_POSTS = 18
MATERIAL_RESETPASSWORD = 19
MATERIAL_ADV_IN_ARTICLE = 20
MATERIAL_POLL = 21
MATERIAL_ADV_MIDDLE = 22
MATERIAL_TYPES = (
    (MATERIAL_TYPE_ADV, _ul(u'Рекламодателям')),
    (MATERIAL_TYPE_RULES, _ul(u'Правила и авторские права')),
    (MATERIAL_TYPE_FEEDBACK, _ul(u'Контакт с администрацией')),
    (MATERIAL_LOGIN, _ul(u'Авторизация')),
    (MATERIAL_REGISTRATION, _ul(u'Регистрация')),
    (MATERIAL_CHANGEPASSWORD, _ul(u'Изменить пароль')),
    (MATERIAL_RESETPASSWORD, _ul(u'Сбросить пароль')),
    (MATERIAL_ABOUT, _ul(u'О нас')),
    (MATERIAL_CREATE_POST, _ul(u'Предложить свою статью')),
    (MATERIAL_CREATE_QUESTION, _ul(u'Задать вопрос')),
    (MATERIAL_NOTES, _ul(u'Знаете ли вы')),
    (MATERIAL_JOKES, _ul(u'Анекдот дня')),
    (MATERIAL_COMMENT_POSTS, _ul(u'Комментируемые статьи')),
    (MATERIAL_QUESTION_POSTS, _ul(u'Бесплатная помощь')),
    (MATERIAL_NEW_POSTS, _ul(u'Новые интересные статьи на портале')),
    (MATERIAL_PRACTIC_POSTS, _ul(u'Практические советы')),
    (MATERIAL_ADV_RIGHT, _ul(u'Реклама справа')),
    (MATERIAL_ADV_IN_ARTICLE, _ul(u'Реклама в статье')),
    (MATERIAL_ADV_TOP, _ul(u'Реклама сверху')),
    (MATERIAL_ADV_MIDDLE, _ul(u'Реклама посередине')),
    (MATERIAL_NEWS_POSTS, _ul(u'Новости')),
    (MATERIAL_POLL, _ul(u'Опрос')),
)
MATERIAL_TYPES_WITHOUT_WYSIWYG = (
    MATERIAL_ADV_RIGHT,
    MATERIAL_ADV_IN_ARTICLE,
    MATERIAL_ADV_TOP,
    MATERIAL_ADV_MIDDLE
)
MATERIALS = {
    '*': {
        'notes': MATERIAL_NOTES,
        'jokes': MATERIAL_JOKES,
        'comment_posts': MATERIAL_COMMENT_POSTS,
        'question_posts': MATERIAL_QUESTION_POSTS,
        'adv_top': MATERIAL_ADV_TOP,
        'adv_middle': MATERIAL_ADV_MIDDLE,
        'adv_right': MATERIAL_ADV_RIGHT,
        'adv_in_article': MATERIAL_ADV_IN_ARTICLE,
        'poll': MATERIAL_POLL,
    },
    'index': {
        'about': MATERIAL_ABOUT,
        'new_posts': MATERIAL_NEW_POSTS,
        'practic_posts': MATERIAL_PRACTIC_POSTS,
    },
    'u-login': {
        'material': MATERIAL_LOGIN,
    },
    'u-registration': {
        'material': MATERIAL_REGISTRATION,
    },
    'u-reset-password': {
        'material': MATERIAL_RESETPASSWORD,
    },
    'u-reset-password-uuid': {
        'material': MATERIAL_RESETPASSWORD,
    },
    'u-password': {
        'material': MATERIAL_CHANGEPASSWORD,
    },
    'u-questions-create': {
        'material': MATERIAL_CREATE_QUESTION,
    },
    'feedback': {
        'material': MATERIAL_TYPE_FEEDBACK,
    },
    'advertisers': {
        'material': MATERIAL_TYPE_ADV,
    },
    'rules': {
        'material': MATERIAL_TYPE_RULES,
    },
}
