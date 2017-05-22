# Getting Started

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
