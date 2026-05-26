import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


# =========================================================
# CONFIGURATION GENERALE
# =========================================================

SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    os.getenv("SECRET_KEY", "django-insecure-change-me-in-production")
)

DEBUG = os.getenv("DJANGO_DEBUG", os.getenv("DEBUG", "1")) == "1"

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        "DJANGO_ALLOWED_HOSTS",
        os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1,0.0.0.0")
    ).split(",")
    if host.strip()
]


# =========================================================
# APPLICATIONS
# =========================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Applications locales
    "accounts",
    "products",
    "cart",
    "orders",
    "dashboard",
    "recommendation",
    "reviews",
]


# =========================================================
# MIDDLEWARE
# =========================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # WhiteNoise pour servir les fichiers statiques en déploiement
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "kbeauty_shop.urls"


# =========================================================
# TEMPLATES
# =========================================================

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

                # Panier
                "cart.context_processors.cart_count",
            ],
        },
    },
]


WSGI_APPLICATION = "kbeauty_shop.wsgi.application"


# =========================================================
# BASE DE DONNEES
# =========================================================
# Par défaut : MySQL, comme demandé dans l'atelier Docker.
# En local, tu peux utiliser SQLite avec USE_SQLITE=True dans .env.

if os.getenv("USE_SQLITE", "False") == "True":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.getenv("MYSQL_DATABASE", "DB_ECOMMERCE"),
            "USER": os.getenv("MYSQL_USER", "django"),
            "PASSWORD": os.getenv("MYSQL_PASSWORD", "django"),
            "HOST": os.getenv("MYSQL_HOST", "db"),
            "PORT": os.getenv("MYSQL_PORT", "3306"),
            "OPTIONS": {
                "charset": "utf8mb4",
            },
        }
    }


# =========================================================
# VALIDATION DES MOTS DE PASSE
# =========================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"
    },
]


# =========================================================
# INTERNATIONALISATION
# =========================================================

LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "Africa/Casablanca"

USE_I18N = True
USE_TZ = True


# =========================================================
# FICHIERS STATIQUES ET MEDIA
# =========================================================
# L'atelier demande STATIC_ROOT, MEDIA_URL et MEDIA_ROOT.
# WhiteNoise utilise STATIC_ROOT après collectstatic.

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# =========================================================
# AUTHENTIFICATION
# =========================================================

LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"


# =========================================================
# CONFIGURATION DJANGO
# =========================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# =========================================================
# SECURITE UPLOADS
# =========================================================

FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024
DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024


# =========================================================
# SECURITE PRODUCTION
# =========================================================
# Attention : sur Oracle VM sans HTTPS, ne mets pas SECURE_SSL_REDIRECT=True.
# Sinon le site peut ne plus s'ouvrir en http://IP_PUBLIQUE.

if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"

    SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "False") == "True"
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "False") == "True"
    CSRF_COOKIE_SECURE = os.getenv("CSRF_COOKIE_SECURE", "False") == "True"


# =========================================================
# CSRF TRUSTED ORIGINS
# =========================================================
# Utile plus tard si Oracle VM utilise un domaine ou une IP publique avec HTTPS.

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]