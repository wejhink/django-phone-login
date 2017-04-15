DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}

INSTALLED_APPS = [

    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',

    'rest_framework',
    'rest_framework.authtoken',

    'phone_login',

    'tests',
]

MIDDLEWARE_CLASSES = []

SECRET_KEY = 'secretkey'
