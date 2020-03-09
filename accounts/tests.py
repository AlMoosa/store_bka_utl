from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserTest(APITestCase):

    def test_user_create(self):
        url = reverse('signup_url')
        data = {'username': 'whatever',
                'password': '12345678',
                'email': 'mail@mail.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.get(id=1).username, 'whatever')
