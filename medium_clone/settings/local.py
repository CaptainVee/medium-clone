from .base import *  # noqa
from .base import env

DEBUG = True

SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="django-insecure-8$q(_*el(vcq$d032d-=_=$)qf!$@)4y-6p9r1fw3janex1$#1",
)

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

CSRF_TRUSTED_ORIGINS = ["http://localhost:8080"]

EMAIL_BACKENDS = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = env("EMAIL_HOST", default="mailhog")
EMAIL_PORT = env("EMAIL_PORT")
DEFAULT_FROM_EMAIL = "support@captainvee.site"
DOMAIN = env("DOMAIN")
SITE_NAME = "Medium"
