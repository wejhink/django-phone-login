import datetime
import uuid

from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.contrib.auth.backends import ModelBackend

from ..utils import model_field_attr
from ..models import PhoneToken

class PhoneBackend(ModelBackend):


    def __init__(self, *args, **kwargs):
        self.user_model = get_user_model()

    def get_username(self):
        """
        Returns a UUID-based 'random' and unique username.

        This is required data for user models with a username field.
        """
        return str(uuid.uuid4())[:model_field_attr(self.user_model, 'username', 'max_length')]

    def authenticate(self, otp=None, **credentials):
        phone_number = credentials.get("phone_number")
        phone_token = PhoneToken.objects.filter(
            phone_number=phone_number,
            used=False,
            timestamp__gte=datetime.datetime.now() - datetime.timedelta(minutes=getattr(settings, 'PHONE_LOGIN_MINUTES', 10))
        ).order_by("-timestamp").first()
        if otp and phone_token and phone_token.otp == otp:
            User = get_user_model()
            user = User.objects.filter(phone_number=phone_number).first()
            if not user:
                password = User.objects.make_random_password()
                user = User.objects.create_user(
                    username=self.get_username(),
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
