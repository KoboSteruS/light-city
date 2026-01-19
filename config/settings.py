"""
Настройки Django проекта 'Яркий Город'.

Production-ready конфигурация с усиленной безопасностью.
"""

from pathlib import Path
from decouple import config, Csv
import os
from loguru import logger

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Security Settings
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'corsheaders',
    'ckeditor',
    'ckeditor_uploader',
    'sorl.thumbnail',
    'axes',
    
    # Local apps
    'apps.core',
    'apps.main',
    'apps.services',
    'apps.portfolio',
    'apps.contacts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'apps.core.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 10}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Разные storage для dev и production
if DEBUG:
    # В режиме разработки - обычный storage без манифеста
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
else:
    # В production - WhiteNoise с манифестом и сжатием
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CKEditor Settings
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight'],
            ['Link', 'Unlink'],
            ['RemoveFormat', 'Source']
        ],
        'height': 300,
        'width': '100%',
    },
}

# Security Settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=False, cast=bool)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=False, cast=bool)
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=False, cast=bool)

# Django Axes - защита от брутфорса
AXES_ENABLED = True
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1  # час
AXES_LOCKOUT_PARAMETERS = [["username", "ip_address"]]
AXES_RESET_ON_SUCCESS = True
# Отключаем access log, чтобы избежать проблем с session_hash
AXES_DISABLE_ACCESS_LOG = True
# Используем только IP для логирования
AXES_IPWARE_META_PRECEDENCE_ORDER = (
    'HTTP_X_FORWARDED_FOR',
    'X_FORWARDED_FOR',
    'HTTP_CLIENT_IP',
    'HTTP_X_REAL_IP',
    'HTTP_X_FORWARDED',
    'HTTP_X_CLUSTER_CLIENT_IP',
    'HTTP_FORWARDED_FOR',
    'HTTP_FORWARDED',
    'HTTP_VIA',
    'REMOTE_ADDR',
)

# Authentication backends
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',  # Должен быть первым
    'django.contrib.auth.backends.ModelBackend',
]

# Custom admin URL
ADMIN_URL = config('ADMIN_URL', default='admin/')

# Email configuration
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@yarko-gorod.ru')

# JWT Settings
JWT_SECRET_KEY = config('JWT_SECRET_KEY', default=SECRET_KEY)
JWT_ALGORITHM = config('JWT_ALGORITHM', default='HS256')
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = config('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', default=30, cast=int)

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 12,
}

# CORS Settings
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='http://localhost:3000', cast=Csv())

# Logging with Loguru
LOG_LEVEL = config('LOG_LEVEL', default='INFO')
LOG_TO_FILE = config('LOG_TO_FILE', default=True, cast=bool)
LOG_TO_CONSOLE = config('LOG_TO_CONSOLE', default=True, cast=bool)
LOG_FILE_MAX_SIZE = config('LOG_FILE_MAX_SIZE', default='10 MB')
LOG_RETENTION_DAYS = config('LOG_RETENTION_DAYS', default=30, cast=int)
LOG_ERROR_RETENTION_DAYS = config('LOG_ERROR_RETENTION_DAYS', default=90, cast=int)

# Настройка loguru
logger.remove()  # Удаляем стандартный обработчик

# Создаем папку для логов, если её нет
LOGS_DIR = BASE_DIR / 'logs'
try:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
except Exception as e:
    print(f'⚠️  Не удалось создать папку logs: {e}')

# Логи в файл (все уровни)
if LOG_TO_FILE:
    try:
        logger.add(
            LOGS_DIR / 'yarko_gorod.log',
            rotation=LOG_FILE_MAX_SIZE,
            retention=f'{LOG_RETENTION_DAYS} days',
            level=LOG_LEVEL,
            format='{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}',
            encoding='utf-8',
            enqueue=True,  # Асинхронная запись для производительности
            backtrace=True,  # Полный стек вызовов при ошибках
            diagnose=True,  # Детальная диагностика
        )
    except Exception as e:
        print(f'⚠️  Не удалось настроить логирование в файл yarko_gorod.log: {e}')

    # Логи ошибок отдельно
    try:
        logger.add(
            LOGS_DIR / 'errors.log',
            rotation=LOG_FILE_MAX_SIZE,
            retention=f'{LOG_ERROR_RETENTION_DAYS} days',
            level='ERROR',
            format='{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}',
            encoding='utf-8',
            enqueue=True,
            backtrace=True,
            diagnose=True,
        )
    except Exception as e:
        print(f'⚠️  Не удалось настроить логирование в файл errors.log: {e}')

# Консольный вывод (для systemd/journald)
if LOG_TO_CONSOLE:
    try:
        import sys
        # В production без цветов, в development с цветами
        if DEBUG:
            logger.add(
                sys.stderr,
                level=LOG_LEVEL,
                format='<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> | <level>{message}</level>',
                colorize=True,
            )
        else:
            # Production: простой формат для systemd
            logger.add(
                sys.stderr,
                level=LOG_LEVEL,
                format='{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}',
                colorize=False,
            )
    except Exception as e:
        print(f'⚠️  Не удалось настроить консольное логирование: {e}')

logger.info('Яркий Город - приложение запущено')
logger.info(f'DEBUG={DEBUG}, LOG_LEVEL={LOG_LEVEL}, LOG_TO_FILE={LOG_TO_FILE}, LOG_TO_CONSOLE={LOG_TO_CONSOLE}')

