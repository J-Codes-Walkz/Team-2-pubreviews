import os
from pathlib import Path
from django.contrib.messages import constants as messages
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

DEV_SECRET_KEY = "django-insecure-brum-second-city-pint-dev-key-change-in-prod"
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", DEV_SECRET_KEY)

# Debug defaults to on locally but off on Heroku (which sets DYNO on every dyno),
# so a missing config var can never put the live site into debug mode.
ON_HEROKU = "DYNO" in os.environ
DEBUG = os.environ.get("DJANGO_DEBUG", "False" if ON_HEROKU else "True").lower() in (
    "true",
    "1",
    "yes",
)

# Fail safe: never run the live site with the public development key.
if not DEBUG and SECRET_KEY == DEV_SECRET_KEY:
    raise ImproperlyConfigured("Set the DJANGO_SECRET_KEY config var before running with DEBUG off.")

ALLOWED_HOSTS = [
    h.strip()
    for h in os.environ.get("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
    if h.strip()
]

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]
if not DEBUG and not CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS = [
        f"https://{host.lstrip('.')}"
        for host in ALLOWED_HOSTS
        if host not in ("127.0.0.1", "localhost", "*")
    ]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "axes",
    # Local Apps
    "reviews.apps.ReviewsConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Must be last: blocks logins that django-axes has locked out
    "axes.middleware.AxesMiddleware",
]

# Enable WhiteNoise if installed
try:
    import whitenoise  # noqa: F401
    MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
except ImportError:
    pass

ROOT_URLCONF = "second_city_pint.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "second_city_pint.wsgi.application"

# Database: Defaults to SQLite locally, supports DATABASE_URL for PostgreSQL in production
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

if os.environ.get("DATABASE_URL"):
    import dj_database_url
    DATABASES["default"] = dj_database_url.config(conn_max_age=600, ssl_require=not DEBUG)

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-gb"
TIME_ZONE = "Europe/London"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Uploaded photos go to Cloudinary when CLOUDINARY_URL is set (Heroku, whose disk is
# wiped on every restart), and to the local media/ folder otherwise.
STORAGES = {
    "default": {
        "BACKEND": (
            "cloudinary_storage.storage.MediaCloudinaryStorage"
            if os.environ.get("CLOUDINARY_URL")
            else "django.core.files.storage.FileSystemStorage"
        )
    },
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Authentication Redirects
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "reviews:index"
LOGOUT_REDIRECT_URL = "reviews:index"

# Login rate limiting (django-axes): 5 wrong passwords for one account from one
# address locks that combination out for 1 hour. Covers the site login and /admin.
AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesStandaloneBackend",
    "django.contrib.auth.backends.ModelBackend",
]
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1  # hours
AXES_LOCKOUT_PARAMETERS = [["username", "ip_address"]]
AXES_RESET_ON_SUCCESS = True


def client_ip(request):
    """The visitor's real IP address.

    Heroku's router appends the real address as the LAST X-Forwarded-For entry;
    anything before it came from the browser and can be faked.
    """
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if ON_HEROKU and forwarded:
        return forwarded.split(",")[-1].strip()
    return request.META.get("REMOTE_ADDR")


AXES_CLIENT_IP_CALLABLE = client_ip

# Security Headers & Cookie Hardening
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = "DENY"

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = os.environ.get("DJANGO_SECURE_SSL_REDIRECT", "True").lower() in (
        "true",
        "1",
        "yes",
    )
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# Map Django message levels to Bootstrap 5 alert/toast classes
MESSAGE_TAGS = {
    messages.DEBUG: "secondary",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "danger",
}
