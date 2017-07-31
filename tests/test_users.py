from django.contrib.auth import get_user_model
from django.db import IntegrityError
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

    """
    We check giving the same number with 2 different formats.
    If the number already exist, the second time the user is being created.
    It must give an error.
    """
    def test_phone_number_equals(self):
        phone_number = "+1 (860) 922-9292"
        phone_same_number = "+1 860922-9292"
        user = User.objects.create_user(
            phone_number=phone_number,
            username="iraycd",
            password="random-password"
        )
        self.assertIsNotNone(user)
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                phone_number=phone_same_number,
                username="iraycd2",
                password="random-password"
            )
        self.assertEqual(user.phone_number, phone_number)
        self.assertEqual(user.phone_number, phone_same_number)
        self.assertEqual(CustomUser.objects.count(), 1)
