from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from users.models import User


class RegistrationTestCase(APITestCase):

    data = {
        "username": "test",
        "email": "test@test.ru",
        "password": "test",
        "first_name": "test",
        "last_name": "test",
    }

    def test_registration(self):

        """Тест создания нового пользователя
        post('/api/users/')"""

        response = self.client.post("/api/users/", self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_auth(self):

        """Тест получения токена авторизации по email и password
        post('/auth/token/login/')"""

        self.client.post("/api/users/", self.data)
        response = self.client.post("/api/auth/token/login/", self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProfileTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_1 = User.objects.create_user(
            username="user1",
            email="1@mail.ru",
            first_name="user1",
            last_name="user1",
            password="password",
        )
        cls.user_1.save()
        cls.user_2 = User.objects.create_user(
            username="user2",
            email="2@mail.ru",
            first_name="user2",
            last_name="user2",
            password="password",
        )
        cls.user_2.save()
        cls.token = Token.objects.create(user=cls.user_1)

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_profile_information(self):

        """Тест получения информации пользователей"""

        profile_id = {
            "my_profile": "/api/users/me/",
            "profile_1": "/api/users/1/",
            "profile_2": "/api/users/2/",
        }
        for profile, t_id in profile_id.items():
            with self.subTest(t_id=t_id):
                response = self.client.get(t_id)
                self.assertEqual(response.status_code, status.HTTP_200_OK)
