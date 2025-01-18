from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-&8o%-b4ml$znrgg#=)&329fp^alx(u8nkk7pi_6o%zq8uo!i-_"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CSRF_TRUSTED_ORIGINS = [
    'https://violent-flossie-kandados-48df4464.koyeb.app',
]

'''hay una copia de mi proyecto alojado en un docker y posteriormente subido
 a koyeb para probarlo en internet y otra copia en un vps mio personal alojado en arsys'''

ALLOWED_HOSTS = ['violent-flossie-kandados-48df4464.koyeb.app',
                 '127.0.0.1',
                 'localhost',
                 '0.0.0.0',
                 '192.168.1.69',
                 '217.160.22.236'
                 ]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",  # Herramientas de desarrollo
    # Aplicaciones del proyecto
    'MiFlixApp',
    'usuarios',
]

AUTH_USER_MODEL = 'usuarios.Usuario'

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "MiFlix.urls"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Directorio global de plantillas
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

WSGI_APPLICATION = "MiFlix.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files (uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Login and logout redirects
LOGIN_REDIRECT_URL = 'MiFlixApp:index'
LOGOUT_REDIRECT_URL = 'MiFlixApp:index'
