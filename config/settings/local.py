from .base import *

DEBUG = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

SECRET_KEY = os.environ.setdefault('SECRET_KEY_CONGREGATIONMS', '')