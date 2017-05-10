from django.test import TransactionTestCase

from phone_login.backends.phone_backend import PhoneBackend


class PhoneBackendTest(TransactionTestCase):

    def test_initialization(self):
        phonebackend = PhoneBackend()
        User = phonebackend.user_model
        self.assertEqual(User.objects.count(), 0)
