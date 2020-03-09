from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import RequestsClient, APITestCase

from .models import SizeOfItem, ColorOfItem, Item

User = get_user_model()


class BasketTest(APITestCase):

    def setUp(self):
        User.objects.create(username="TestUser", password='admin', email='qwe@qwe')
        item = Item.objects.create(name='Phone', price=23)
        SizeOfItem.objects.create(name='TestUser', amount=23, price=234, item=item)
        ColorOfItem.objects.create(name='Black', amount=2, price=454, item=item)
        self.user = self.set_up()

    @staticmethod
    def set_up():
        User = get_user_model()
        return User.objects.create_user(
            username='test',
            email='mail@mail.asd',
            password='asdfg'
        )

    def test_create_basket(self):
        url = reverse('basket')
        self.client.login(username='test', password='asdfg')
        data = {
            'size_basket': [1],
            'color_basket': [1],
            'item_basket': [1]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


def test_all_basket():
    client = RequestsClient()
    response = client.get('http://localhost:8000/api/v1/basket/')
    assert response.status_code == 200


class BookingTest(APITestCase):
    def setUp(self):
        item = Item.objects.create(name='iPhone', price=1000)
        SizeOfItem.objects.create(name='TestSize', amount=2, price=14, item=item)
        ColorOfItem.objects.create(name='White', amount=4, price=4, item=item)
        self.user = self.set_up()

    @staticmethod
    def set_up():
        User = get_user_model()
        return User.objects.create_user(
            username='root',
            email='root@root.com',
            password='root'
        )

    def test_booking(self):
        print("test wis")
        url = reverse('basket')
        self.client.login(username='root', password='root')
        data = {
            'size_basket': [1],
            'color_basket': [1],
            'item_basket': [1]
        }
        self.client.post(url, data, format='json')

        url = reverse('booking')
        data = {'delivery': 2}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
