import datetime

from django.conf import settings
from django.test import TransactionTestCase

from phone_login.models import PhoneToken


# Here is where we check the Creation and Generation of OTP.
#
# Creating and Validating OTP
# 1. Success - When phone_number, otp are given and timestamp is within
#    PHONE_LOGIN_OTP_LENGTH limit or 6.
# 2. Failure - When phone_number is not given or class isn't defined
# 3. Failure - When attempts are more more than PHONE_LOGIN_ATTEMPTS or 10.
# 4. Failure - When time range is greater than PHONE_LOGIN_OTP_LENGTH.
# 5. Failure - When OTP is not given.


class PhoneTokenTest(TransactionTestCase):
    phone_token = PhoneToken

    # To check if the developers can create their own implementation on
    # validation.
    def test_check_manual_token(self):
        phone_number = "+01 9212128291"
        otp = '0944'
        token = self.phone_token.objects.create(
            phone_number=phone_number,
            otp=otp
        )
        self.assertEqual(token.otp, otp)

    def test_create_otp_for_number(self):
        phone_number = "+01 9212128291"
        phone_token = self.phone_token.create_otp_for_number(phone_number)

        today_min = datetime.datetime.combine(
            datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(
            datetime.date.today(), datetime.time.max)

        otps = self.phone_token.objects.filter(
            phone_number=phone_number, timestamp__range=(today_min, today_max))
        self.assertTrue(
            otps.count() <= getattr(
                settings, 'PHONE_LOGIN_ATTEMPTS', 10),
            'message')
        self.assertIsNotNone(phone_token, 'Test Created OTP')
        self.assertIsNotNone(phone_token.otp, 'OTP Exists')
