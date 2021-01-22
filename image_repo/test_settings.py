import sys

from .settings import *


# from django.core.management.utils import get_random_secret_key
# print(get_random_secret_key()))
SECRET_KEY = ")4i7=lziie#f&@y=q2r3$j_lpq=!n+*%#tnngnmpk^dc45vuda"

DATABASES["default"]["ENGINE"] = "django.db.backends.sqlite3"
DATABASES["default"]["NAME"] = "db.sqlite3"
if "--keepdb" in sys.argv:
    DATABASES["default"]["TEST"] = {"NAME": "/dev/shm/image-repo-test-db.sqlite3"}