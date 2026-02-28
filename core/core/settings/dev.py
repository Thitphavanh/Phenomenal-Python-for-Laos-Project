"""
Development settings for core project.
ການຕັ້ງຄ່າສຳລັບການພັດທະນາ (Development)

ການໃຊ້ງານ:
export DJANGO_SETTINGS_MODULE=core.settings.dev
python manage.py runserver
"""

from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-isz-6$ft#$_&+$8f33%ah@c$w4380m7lw8drzojpidhtz2&9+$"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*", "localhost", "127.0.0.1"]

# Allow CSRF POST requests from Ngrok URLs
CSRF_TRUSTED_ORIGINS = [
    "https://*.ngrok-free.app",
    "https://*.ngrok.io",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]
# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Development-specific settings

# Show detailed error pages
DEBUG_PROPAGATE_EXCEPTIONS = True

# ============================================================
# SESSION & COOKIE SETTINGS
# ============================================================

# Session engine (database-backed)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Session cookie age: 2 weeks (seconds)
SESSION_COOKIE_AGE = 60 * 60 * 24 * 14  # 14 days

# Session expires when browser closes (False = persistent cookie)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Prevent JavaScript from reading the session cookie
SESSION_COOKIE_HTTPONLY = True

# SameSite policy: Lax protects against CSRF on cross-site requests
SESSION_COOKIE_SAMESITE = 'Lax'

# Do NOT require HTTPS in development (set True in production)
SESSION_COOKIE_SECURE = False

# CSRF cookie settings
CSRF_COOKIE_HTTPONLY = False   # Must be False so JavaScript can read it
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SECURE = False     # Set True in production

# Django Debug Toolbar (if installed)
# INSTALLED_APPS += ["debug_toolbar"]
# MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
# INTERNAL_IPS = ["127.0.0.1"]

# Email backend for development (console output)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Logging configuration for development
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
