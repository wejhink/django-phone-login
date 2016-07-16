import datetime

from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.contrib.auth.backends import ModelBackend

from ..models import PhoneToken

class PhoneBackend(ModelBackend):
    def authenticate(self, otp=None, **credentials):
        phone_number = credentials.get("phone_number")
        phone_token = PhoneToken.objects.filter(
            phone_number=phone_number,
            used=False,
            timestamp__gte=datetime.datetime.now() - datetime.timedelta(minutes=getattr(settings, 'PHONE_LOGIN_MINUTES', 10))
        ).first()
        if otp and phone_token and phone_token.otp == otp:
            User = get_user_model()
            user = User.objects.filter(phone_number=phone_number).first()
            if not user:
                password = User.objects.make_random_password()
                user = User.objects.create_user(
                    username=phone_number,
                    password=password,
                    email="",
                    phone_number=phone_number
                )
            phone_token.used = True
            phone_token.attempts = phone_token.attempts + 1
            phone_token.save()
            return user
        elif otp and phone_token:
            phone_token.attempts = phone_token.attempts + 1
            phone_token.save()
        return None
