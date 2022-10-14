
from .base import * 
from .base import env

DEBUG = True

SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="django-insecure-8$q(_*el(vcq$d032d-=_=$)qf!$@)4y-6p9r1fw3janex1$#1",
)

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]
