from django.contrib.auth import get_user_model
from django.test import TransactionTestCase

from .models import CustomUser

"""
Checking with various custom users.
1. Check if CustomUser is in AUTH_USER_MODEL.
1. User with username and email
2. User with just email
3. User can also have password
"""

User = get_user_model()


class PhoneTokenTest(TransactionTestCase):

    def test_check_auth_user_model(self):
        user = User.objects.create_user(
            phone_number="+01 9212128291",
            username="iraycd",
            password="random-password"
        )
        self.assertIsNotNone(user)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(User.objects.count(), CustomUser.objects.count())
