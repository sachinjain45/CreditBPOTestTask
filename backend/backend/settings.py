import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'your-default-secret-key-for-dev')
DEBUG = True

ALLOWED_HOSTS_STRING = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost 127.0.0.1 backend 0.0.0.0')
ALLOWED_HOSTS = ALLOWED_HOSTS_STRING.split(' ')


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'drf_spectacular', # OpenAPI/Swagger
    'cryptography', # For django-cryptography

    # Local apps
    'core', # For audit logs, utils
    'users',
    'profiles',
    'matching',
    'payments',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # Place it high, but after SessionMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# DATABASES = {
#     'default': {
#         'ENGINE': os.getenv('DATABASE_ENGINE', 'django.db.backends.postgresql'),
#         'NAME': os.getenv('DATABASE_DB', 'creditbpo_db'),
#         'USER': os.getenv('DATABASE_USER', 'creditbpo_user'),
#         'PASSWORD': os.getenv('DATABASE_PASSWORD', 'secret'),
#         'HOST': os.getenv('DATABASE_HOST', 'db'), # 'db' is the service name in docker-compose
#         'PORT': os.getenv('DATABASE_PORT', '5432'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

AUTH_USER_MODEL = 'users.User'

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles' # For collectstatic

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# Simple JWT settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60), # Adjust as needed
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True, # Generates a new refresh token when one is used
    'BLACKLIST_AFTER_ROTATION': True, # Blacklists old refresh token
    'UPDATE_LAST_LOGIN': True,
}

# CORS settings
CORS_ALLOWED_ORIGINS_STRING = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000')
CORS_ALLOWED_ORIGINS = CORS_ALLOWED_ORIGINS_STRING.split(',')
CORS_ALLOW_CREDENTIALS = True # If your frontend sends cookies (e.g., for session-based auth if JWT in cookies)

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': 'json_log_formatter.JSONFormatter',
        },
    },
    'handlers': {
        'json': {
            'class': 'logging.StreamHandler',
            'formatter': 'json',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/app.log',
            'formatter': 'json',
        },
    },
    'loggers': {
        '': {  # Root logger
            'handlers': ['json', 'file'],
            'level': 'INFO',
        },
        'django': {
            'handlers': ['json', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'payments': {
            'handlers': ['json', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Health Check Settings
HEALTH_CHECK = {
    'DISK_USAGE_MAX': 90,  # 90%
    'MEMORY_MIN': 100,     # 100MB
    'DATABASE_TIMEOUT': 5,  # 5 seconds
}

# django-cryptography settings
# IMPORTANT: Store this key securely (e.g., environment variable, secrets manager)
# For multiple fields, you might use multiple keys.
CRYPTOGRAPHY_KEY = os.getenv('DJANGO_CRYPTOGRAPHY_KEY', 'a-very-secret-and-long-random-key-for-encryption')
FIELD_ENCRYPTION_KEYS = [CRYPTOGRAPHY_KEY]


# Caching (Redis)
# Ensure Redis service is running and accessible
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

# Redis cache configuration (optional)
if os.getenv('USE_REDIS_CACHE', 'False') == 'True':
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": os.getenv("REDIS_URL", "redis://redis:6379/1"),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        }
    }

# Stripe settings
# STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
# STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')
# STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')
# STRIPE_REPORT_PRICE_ID = os.getenv('STRIPE_REPORT_PRICE_ID', 'price_...')
# STRIPE_SEEKER_SUB_PRICE_ID = os.getenv('STRIPE_SEEKER_SUB_PRICE_ID', 'price_...')
# STRIPE_PROVIDER_SUB_TIER1_PRICE_ID = os.getenv('STRIPE_PROVIDER_SUB_TIER1_PRICE_ID', 'price_...')

# SendGrid settings
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@example.com')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@example.com') # For notifications

# drf-spectacular settings
SPECTACULAR_SETTINGS = {
    'TITLE': 'CreditBPO Matching Platform API',
    'DESCRIPTION': 'API for Seeker/Provider matching, payments, and profiles.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False, # Schema available at /api/schema/
    # Optional: Add security definitions for JWT
    'SWAGGER_UI_SETTINGS': {
        "deepLinking": True,
        "persistAuthorization": True,
        "displayOperationId": True,
    },
     'APPEND_COMPONENTS': {
        'securitySchemes': {
            'bearerAuth': {
                'type': 'http',
                'scheme': 'bearer',
                'bearerFormat': 'JWT',
            }
        }
    },
    'SECURITY': [{'bearerAuth': []}],
}

# Site URL (for constructing full URLs in emails, Stripe redirects, etc.)
SITE_URL = os.getenv('SITE_URL', 'http://localhost:3000')

FIELD_ENCRYPTION_KEY = "1Trp+dXbqoe3jXNN9ZAqWXHdZrfxinnHO6oL6AQDuOI="