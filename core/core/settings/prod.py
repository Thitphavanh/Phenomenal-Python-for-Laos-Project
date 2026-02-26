"""
Production settings for core project.
ການຕັ້ງຄ່າສຳລັບການ Deploy ຂຶ້ນ Production

ການໃຊ້ງານ:
export DJANGO_SETTINGS_MODULE=core.settings.prod
python manage.py runserver
"""

from .base import *
import os

# SECURITY WARNING: keep the secret key used in production secret!
# ໃຊ້ environment variable ສຳລັບ production
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "CHANGE-THIS-IN-PRODUCTION-USE-ENV-VARIABLE"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    "pythonforlaos.com",
    "www.pythonforlaos.com",
    # ເພີ່ມ domain ຂອງທ່ານເອງ
]


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# ຕົວຢ່າງການໃຊ້ PostgreSQL ສຳລັບ Production
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "pythonforlaos_db"),
        "USER": os.environ.get("DB_USER", "postgres"),
        "PASSWORD": os.environ.get("DB_PASSWORD", ""),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}

# ຫຼື ຖ້າຍັງໃຊ້ SQLite ສຳລັບ production ນ້ອຍໆ
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }


# Security Settings for Production

# HTTPS Settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HSTS Settings
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Other Security Settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"


# Static Files for Production
# ໃຊ້ WhiteNoise ສຳລັບ serve static files
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# Email Configuration for Production
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "noreply@pythonforlaos.com")


# Logging for Production
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs" / "django.log",
            "formatter": "verbose",
        },
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["file", "console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}


# Cache Configuration (ຖ້າຕ້ອງການ)
# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.redis.RedisCache",
#         "LOCATION": os.environ.get("REDIS_URL", "redis://127.0.0.1:6379/1"),
#     }
# }


# Admin URL (ປ່ຽນເປັນ URL ທີ່ຍາກເດົາສຳລັບຄວາມປອດໄພ)
# ຕ້ອງປ່ຽນໃນ core/urls.py ດ້ວຍ
# ADMIN_URL = os.environ.get("ADMIN_URL", "secret-admin/")
