from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from phone_login.models import PhoneToken


class PhoneTokenGenerationTests(APITestCase):
    url = reverse('phone_login:generate')
    data = {'phone_number': '+919052500315'}
    invalid_data = {'phone_number': ''}

    def test_token_generation(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(PhoneToken.objects.count(), 1)

    def test_db_generation(self):
        self.assertEqual(PhoneToken.objects.count(), 0)

    def test_extra_attempts(self):
        settings.PHONE_LOGIN_ATTEMPTS = 1
        self.client.post(self.url, self.data, format='json')
        self.client.post(self.url, self.data, format='json')
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_data(self):
        response = self.client.post(self.url, self.invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
