import datetime
import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from ..models import PhoneToken
from ..utils import model_field_attr


class PhoneBackend(ModelBackend):
    def __init__(self, *args, **kwargs):
        self.user_model = get_user_model()

    def get_username(self):
        """
        Returns a UUID-based 'random' and unique username.

        This is required data for user models with a username field.
        """
        return str(uuid.uuid4())[:model_field_attr(
            self.user_model, 'username', 'max_length')
               ]

    def create_user(self, phone_token, **extra_fields):
        """
        Create and returns the user based on the phone_token.
        """
        password = self.user_model.objects.make_random_password()
        if extra_fields.get('username'):
            username = extra_fields.get('username')
        else:
            username = self.get_username()
        if extra_fields.get('password'):
            password = extra_fields.get('password')
        else:
            password = password
        phone_number = phone_token.phone_number
        user = self.user_model.objects.create_user(
            username=username,
            password=password,
            phone_number=phone_number
        )
        return user

    def authenticate(self, request, pk=None, otp=None, **extra_fields):

        # 1. Validating the PhoneToken with PK and OTP.
        # 2. Check if phone_token and otp are same, within the given time range
        timestamp_difference = datetime.datetime.now() - datetime.timedelta(
            minutes=getattr(settings, 'PHONE_LOGIN_MINUTES', 10)
        )
        try:

            phone_token = PhoneToken.objects.get(
                pk=pk,
                otp=otp,
                used=False,
                timestamp__gte=timestamp_difference
            )
        except PhoneToken.DoesNotExist:
            phone_token = PhoneToken.objects.get(pk=pk)
            phone_token.attempts = phone_token.attempts + 1
            phone_token.save()
            raise PhoneToken.DoesNotExist

        # 3. Create new user if he doesn't exist. But, if he exists login.
        user = self.user_model.objects.filter(
            phone_number=phone_token.phone_number
        ).first()
        if not user:
            user = self.create_user(
                phone_token=phone_token,
                **extra_fields
            )
        phone_token.used = True
        phone_token.attempts = phone_token.attempts + 1
        phone_token.save()
        return user
