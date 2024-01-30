from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from news.models import BlogPost
from users.models import User


class AddingNewsTestCase(APITestCase):

    data = {
        "title": "test",
        "text": "test",
    }

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword",
        )
        cls.token = Token.objects.create(user=cls.user)

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_adding_news(self):

        """Тест создания нового пользователя
        post('/api/news/')"""

        response = self.client.post("/api/news/", self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        news_count = BlogPost.objects.filter(title=self.data['title']).count()
        self.assertEqual(news_count, 1)


