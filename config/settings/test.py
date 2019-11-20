from .local import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

_db = os.path.join(BASE_DIR, 'test.sqlite3')
DATABASES['default']['NAME'] = _db
