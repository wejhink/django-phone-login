from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from phone_login.models import PhoneToken


class PhoneTokenGenerationTests(APITestCase):

    def test_token_generation(self):
        url = reverse('phone_login:generate')
        data = {'phone_number': '+919052500315'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(PhoneToken.objects.count(), 1)

    def test_db_generation(self):
        self.assertEqual(PhoneToken.objects.count(), 0)
