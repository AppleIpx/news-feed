from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from news.models import Comment, BlogPost
from users.models import User


class AddingNewsTestCase(APITestCase):

    data = {
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

    def test_adding_comments(self):

        """Тест создания нового нового комментария
        post('/api/news/3/comments')"""
        blog_post = BlogPost.objects.create(title="Test Post", text="Test Post Text")

        response = self.client.post(f"/api/news/{blog_post.id}/comments/", self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg="Failed to create a comment")

        # Проверяем, что комментарий действительно создан
        comments_count = Comment.objects.filter(blog_post=blog_post).count()
        self.assertEqual(comments_count, 1, msg="Incorrect number of comments for the post")

