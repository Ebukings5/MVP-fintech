import os
import environ
from celery.schedules import crontab
from pathlib import Path

# Initialize environment variables
env = environ.Env()
environ.Env.read_env()  # Read .env file

# Define BASE_DIR as a Path object
BASE_DIR = Path(__file__).resolve().parent.parent

# URL configuration
ROOT_URLCONF = 'finance_manager.urls'

# Installed apps
INSTALLED_APPS = [
    'core',
    'rest_framework',
    'rest_framework_simplejwt',
    'django_celery_beat',
    'finance_manager',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.staticfiles',
    'django.contrib.sessions',
    'django.contrib.messages',
]

# CORS configuration
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',  # Add your frontend URL
]

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Correctly set the static root

# Default auto field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Secret key
SECRET_KEY = env('DJANGO_SECRET_KEY', default='default_secret_key')

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.ValidateRequestMiddleware',  # Ensure these are implemented
    'core.middleware.CustomMiddleware',  # Ensure this matches your actual class and path
]

# Custom user model
AUTH_USER_MODEL = 'finance_manager.CustomUser'

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='default_email@example.com')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='default_password')

# Celery configuration
CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND', default='redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# Celery beat schedule
CELERY_BEAT_SCHEDULE = {
    'send-upcoming-bill-notifications-every-morning': {
        'task': 'core.tasks.send_upcoming_bill_notifications',
        'schedule': crontab(hour=8, minute=0),
    },
    'send-budget-limit-alerts-every-evening': {
        'task': 'core.tasks.send_budget_limit_alerts',
        'schedule': crontab(hour=18, minute=0),
    },
}

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME', default='finance_manager'),
        'USER': env('DB_USER', default='chukwuebuka'),
        'PASSWORD': env('DB_PASSWORD', default='Icui4cu2'),
        'HOST': 'db' if os.getenv('IN_DOCKER') else 'localhost',  # Use 'localhost' locally and 'db' in Docker
        'PORT': env.int('DB_PORT', default=5432),
    }
}

# REST framework configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'EXCEPTION_HANDLER': 'core.views.custom_exception_handler',
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# Templates configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Ensure template directory is set
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Debug settings
DEBUG = env.bool('DJANGO_DEBUG', default=False)  # Set dynamically based on env variable
ALLOWED_HOSTS = env('DJANGO_ALLOWED_HOSTS', default='*').split(',')  # Adjust for production
