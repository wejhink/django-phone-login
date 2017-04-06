# Django Phone Login


This login is basically used to login via OTP using `phone_number` as the new field instead of using `email` or `username` as the login.

## How does it work?

We use [django-sendsms][django-sendsms] to the phone and OTP and Verify it.
This way you can use your favorite SMS Service.
You can ask the user for `phone_number` using Forms as authentication and login in any web browser. By sending the OTP.
Second, you can use `Django Rest Framework` and login like how Whatsapp, Viber and many login works.


### Example.

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
