# Django Phone Login

Django Phone Login provides phone number login with no additional passwords to remember.
It's a easy way to grow your customer base. Without any hassle.

## Why use django-phone-login?

+ Phone number login, no password required.
+ Registration through phone number.
+ Mobile based user authentication.

# Flow
1. User enter the `phone_number` and sends request to generate `secret code`.
1. `django-phone-login` sends a `secret_code` as SMS to the phone number.
1. User sends `secret_code` to the server to verify.
1. `django-phone-login` verifies and send `token` as response using `DRF3`.


### Installation

`pip install django-phone-login`

### Instructions

Add the Below `urls.py`

```python
urlpatterns = [
    url(r'^otp/', include('phone_login.urls', namespace='phone_login'),),
]
```

Make the following changes in the `settings.py`

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


AUTH_USER_MODEL = 'phone_login.CustomUser'

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
```

## Development
Coming Up...

# Requirement

+ [Django]
+ [django-phonenumber-field]
+ [Django Rest Framework]


# Customizable Fields in Settings.

```python
PHONE_LOGIN_MINUTES = 10
PHONE_LOGIN_OTP_LENGTH = 6
PHONE_LOGIN_OTP_HASH_ALGORITHM = 'sha256'
```


[django]: https://github.com/django/django
[django-sendsms]: https://github.com/stefanfoulis/django-sendsms
[django-phonenumber-field]: https://github.com/stefanfoulis/django-phonenumber-field "Django PhoneNumber Field"
[Django Rest Framework]: https://github.com/tomchristie/django-rest-framework
