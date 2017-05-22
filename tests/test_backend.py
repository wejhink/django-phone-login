from django.test import TransactionTestCase

from phone_login.models import PhoneToken
from phone_login.backends.phone_backend import PhoneBackend


class PhoneBackendTest(TransactionTestCase):

    def test_initialization(self):
        phonebackend = PhoneBackend()
        User = phonebackend.user_model
        self.assertEqual(User.objects.count(), 0)

    def test_authenticate_registration(self):
        phonebackend = PhoneBackend()
        phone_number = "+18609409290"
        token = PhoneToken.create_otp_for_number(phone_number)
        user = phonebackend.authenticate(pk=token.id, otp=token.otp)
        self.assertEqual(user.phone_number, phone_number, 'Signup phonenumber')

    def test_authenticate_login(self):
        phonebackend = PhoneBackend()
        phone_number = "+18609409290"
        phone_token = PhoneToken.create_otp_for_number(phone_number)
        user = phonebackend.create_user(
            phone_token=phone_token
        )
        self.assertEqual(user.phone_number, phone_number, 'User creation')
        authenticated_user = phonebackend.authenticate(
            pk=phone_token.id,
            otp=phone_token.otp
        )
        self.assertEqual(
            authenticated_user.phone_number,
            phone_number,
            'Login phonenumber'
        )
