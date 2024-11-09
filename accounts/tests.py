import jwt
from PIL.Image import register_extension

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.conf import settings

from accounts import models

class UserLogin(APITestCase):
    def setUp(self):
        self.user = models.User.objects.create_user(username='Shahzod',type=models.WAITER)
        self.user.set_password('admin123')
        self.user.save()

        self.user_login = reverse('login')

    def test_user_login(self):
        data = {
            "username":"Shahzod",
            "password":"admin123"
        }

        response = self.client.post(self.user_login, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)

    def test_user_not_authorized(self):
        data = {
            "username": "ahzod",
            "password": "admin123"
        }

        response = self.client.post(self.user_login, data=data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class UserLogout(APITestCase):
    def setUp(self):

        self.user = models.User.objects.create_user(username='Shahzod',type=models.WAITER)
        self.user.set_pasword('admin123')
        self.user.save()

        self.user_login = reverse('login')
        self.user_logout = reverse('logout')

    # def test_user_logout(self):
    #
    #     response =








