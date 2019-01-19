[![build-status-image]][travis]
[![pypi-version]][pypi]

# Django Phone Login

Django-phone-login uses django-sendsms to send sms.

Django Phone Login provides phone number login with no additional passwords to remember.
It's a easy way to grow your customer base. Without any hassle.


## Installing Django Phone Login

Django Phone Login was built for django.

PyPi, install using PIP:

```bash
pip install django-phone-login
```

If you want to install manually:

```bash
git clone git@github.com:wejhink/django-phone-login.git
cd django-phone-login/
pip install -r requirements.txt
python setup.py install
```

## Instructions

```python
INSTALLED_APPS += [
    ...  # Make sure to include the default installed apps here.

    'phone_login',
    'rest_framework',
    'rest_framework.authtoken',
]


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    )
}



AUTHENTICATION_BACKENDS = [
    'phone_login.backends.phone_backend.PhoneBackend',
    'django.contrib.auth.backends.ModelBackend'
]

# Make sure you also have backend Django Templates and APP_DIRS True, if you want to use default OTP Template.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        ...
    },
]


# Configure the SENDSMS_BACKEND (for django-sendsms integration)

SENDSMS_BACKEND = 'myapp.mysmsbackend.SmsBackend' #(defaults to 'sendsms.backends.console.SmsBackend')
SENDSMS_FROM_NUMBER = "+XXxxxxxxxxxx" 
SENDSMS_ACCOUNT_SID = 'ACXXXXXXXXXXXXXX'
SENDSMS_AUTH_TOKEN = 'xxxxxxxx' 

```

## Adding to URLs

Add the Below `urls.py`

```python
urlpatterns = [
    url(r'^phone_login/', include('phone_login.urls', namespace='phone_login'),),
]
```

## Customizable Fields in Settings.

```python
PHONE_LOGIN_ATTEMPTS = 10
PHONE_LOGIN_OTP_LENGTH = 6
PHONE_LOGIN_OTP_HASH_ALGORITHM = 'sha256'
PHONE_LOGIN_DEBUG = True  # will include otp in generate response, default is False.
```


# Flow
1. User enter the `phone_number` and sends request to generate `secret code`.
1. `django-phone-login` sends a `secret_code` as SMS to the phone number.
1. User sends `secret_code` to the server to verify.
1. `django-phone-login` verifies and send `token` as response using `DRF3`.



## Why use django-phone-login?

+ Phone number login, no password required.
+ Registration through phone number.
+ Mobile based user authentication.


[build-status-image]: https://secure.travis-ci.org/wejhink/django-phone-login.svg?branch=master
[travis]: http://travis-ci.org/wejhink/django-phone-login?branch=master
[pypi-version]: https://img.shields.io/pypi/v/django-phone-login.svg
[pypi]: https://pypi.python.org/pypi/django-phone-login
