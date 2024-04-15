import os
from dotenv import load_dotenv
from split_settings.tools import include
from pathlib import Path

load_dotenv()

include(
    "components/database.py",
    "components/installed_apps.py",
    "components/middleware.py",
    "components/templates.py",
    "components/logging.py",
)
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = os.environ.get("DEBUG", False)

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(",")

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"

LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOCALE_PATHS = ["movies/locale"]

INTERNAL_IPS = ["127.0.0.1"]

STATIC_ROOT = "app/static"

CORS_ALLOWED_ORIGINS = ["http://127.0.0.1"]
