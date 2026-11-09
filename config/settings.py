"""
二手書交易平台的 Django 設定。

密鑰與開發選項從 repo 根目錄的 .env 讀取（範例見 .env.example），
程式碼與設定檔不提交任何密鑰（constitution v2.0.0 資料安全）。
"""

import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    raise ImproperlyConfigured(
        "找不到 DJANGO_SECRET_KEY。請把 .env.example 複製成 .env 並填入密鑰。"
    )

DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]


# Application definition

INSTALLED_APPS = [
    # 後台主題，必須放在 django.contrib.admin 之前（research R-08）
    "unfold",
    "unfold.contrib.filters",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.accounts",
    "apps.catalog",
    "apps.orders",
    "apps.messaging",
    "apps.favorites",
    "apps.backoffice",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database：SQLite（research R-01）

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# 使用者與登入

AUTH_USER_MODEL = "accounts.User"

LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Email：驗證信存成本機檔案，不真的寄出（research R-01）

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / os.environ.get("EMAIL_FILE_PATH", "sent_emails")
DEFAULT_FROM_EMAIL = "noreply@example.com"


# Internationalization

LANGUAGE_CODE = "zh-hant"
TIME_ZONE = "Asia/Taipei"
USE_I18N = True
USE_TZ = True


# Static files 與上傳檔案

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"


# 後台主題 django-unfold：與前台共用青綠色品牌色（research R-08）

UNFOLD = {
    "SITE_TITLE": "二手書交易平台 後台",
    "SITE_HEADER": "二手書交易平台",
    "SITE_SUBHEADER": "管理後台",
    "SITE_SYMBOL": "menu_book",
    "SITE_URL": "/",
    "SHOW_HISTORY": True,
    "COLORS": {
        "primary": {
            "50": "oklch(98.4% .014 180.72)",
            "100": "oklch(95.3% .051 180.801)",
            "200": "oklch(91% .096 180.426)",
            "300": "oklch(85.5% .138 181.071)",
            "400": "oklch(77.7% .152 181.912)",
            "500": "oklch(70.4% .14 182.503)",
            "600": "oklch(60% .118 184.704)",
            "700": "oklch(51.1% .096 186.391)",
            "800": "oklch(43.7% .078 188.216)",
            "900": "oklch(38.6% .063 188.416)",
            "950": "oklch(27.7% .046 192.524)",
        },
    },
}


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
