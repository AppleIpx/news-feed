from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from users.models import User
from django.core import exceptions as django_exceptions
from rest_framework.authtoken.models import Token
from news.models import (
    BlogPost,
    Comment,
)
from news.models import Comment


# ---------start-users------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
        )


class PasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)

    def validate(self, value):
        try:
            validate_password(value['new_password'])
        except django_exceptions.ValidationError as e:
            raise serializers.ValidationError(
                {'new_password': list(e.messages)}
            )
        return super().validate(value)

    class Meta:
        model = User
        fields = "__all__"


class TokenSerializer(serializers.ModelSerializer):
    token = serializers.CharField(source="key")

    class Meta:
        model = Token
        fields = ("token",)


# --------end-users----------


# ----------start-news-------


class ShowNewsListSerializer(serializers.ModelSerializer):
    """Без комментариев"""
    user = UserSerializer(read_only=True)

    class Meta:
        model = BlogPost
        fields = (
            "title",
            "image",
            "text",
            "created_at",
            'user',
        )


class ShowNewsSerializer(serializers.ModelSerializer):
    """C комментариями"""
    user = UserSerializer(read_only=True)
    comments = serializers.SerializerMethodField("get_comments")

    class Meta:
        model = BlogPost
        fields = (
            "title",
            "image",
            "text",
            'user',
            'comments',
        )

    def get_comments(self, obj):
        comments = Comment.objects.filter(blog_post=obj)
        return CommentsSerializers(comments, many=True).data


class CommentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ['user', 'blog_post']


class CreateNewsSerializers(serializers.ModelSerializer):
    image = serializers.ImageField(
        required=False,
        allow_empty_file=True,
        default=None
    )
    class Meta:
        model = BlogPost
        fields = [
            'id',
            'title',
            'image',
            'text',
            'created_at',
        ]
# ----------end-news---------
