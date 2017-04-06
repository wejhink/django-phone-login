from __future__ import unicode_literals

import datetime
import hashlib
import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from sendsms.message import SmsMessage


class PhoneNumberAbstactUser(AbstractUser):

    phone_number = PhoneNumberField(unique=True)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

class CustomUser(PhoneNumberAbstactUser):

    REQUIRED_FIELDS = ['phone_number', 'email']

    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.username


class PhoneToken(models.Model):

    phone_number = PhoneNumberField(editable=False)
    otp = models.CharField(max_length=40, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    attempts = models.IntegerField(default=0)
    used = models.BooleanField(default=False)

    class Meta:
        verbose_name = "OTP Token"
        verbose_name_plural = "OTP Tokens"

    def __str__(self):
        return "{} - {}".format(self.phone_number, self.otp)

    @classmethod
    def create_otp_for_number(cls, number):
        # The max otps generated for a number in a day are only 10.
        # Any more than 10 attempts returns False for the day.
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        otps = cls.objects.filter(phone_number=number, timestamp__range=(today_min, today_max))
        if otps.count() <= 10:
            otp = cls.generate_otp(length=getattr(settings, 'PHONE_LOGIN_OTP_LENGTH', 6))
            phone_token = PhoneToken(phone_number=number, otp=otp)
            phone_token.save()
            message = SmsMessage(
                            body=render_to_string("otp_sms.txt", {"otp":otp, "id":phone_token.id}),
                            to=[number]
                        )
            message.send()
            return phone_token
        else:
            return False

    @classmethod
    def generate_otp(cls, length=6):
        hash_algorithm = getattr(settings, 'PHONE_LOGIN_OTP_HASH_ALGORITHM', 'sha256')
        m = getattr(hashlib, hash_algorithm)()
        m.update(getattr(settings, 'SECRET_KEY', None).encode('utf-8'))
        m.update(os.urandom(16))
        otp = str(int(m.hexdigest(), 16))[-length:]
        return otp
