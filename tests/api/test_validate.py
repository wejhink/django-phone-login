from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from phone_login.models import PhoneToken

User = get_user_model()


class PhoneTokenValidationTests(APITestCase):

    def test_token_validation(self):
        # Generate a token with phone number
        phone_number = "+01 9212128291"
        otp = '0944'
        token = PhoneToken.objects.create(
            phone_number=phone_number,
            otp=otp
        )
        self.assertIsNotNone(token.pk)
        url = reverse('phone_login:validate')
        data = {'pk': token.pk, 'otp': otp}
        response = self.client.post(url, data, format='json')
        self.assertIsNotNone(response.data['token'])
        self.assertIsNotNone(response.data['status'], status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)

    def test_token_validation_with_custom_field(self):
        # Generate a token and test it with custom models.
        pass
