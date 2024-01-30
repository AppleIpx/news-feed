from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.throttling import (
    UserRateThrottle,
    AnonRateThrottle,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework import serializers
from .serializers import (
    UserSerializer,
    PasswordSerializer,
    CreateNewsSerializers,
    ShowNewsSerializer,
    ShowNewsListSerializer, CommentsSerializers,
)
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .filters import NewsFilter
from users.models import User
from news.models import BlogPost
from . tasks import thanks_for_sing_up


# ----------start-users-----

class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    @action(
        methods=["get"],
        detail=False,
        permission_classes=(IsAuthenticatedOrReadOnly,)
    )
    def me(self, request):
        user = get_object_or_404(
            User,
            pk=request.user.id
        )
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def perform_create(self, serializer):
        if "password" in self.request.data:
            password = make_password(self.request.data["password"])
            serializer.save(password=password)
            thanks_for_sing_up.delay(
                serializer.data.get("first_name"),
                serializer.data.get("email"),
            )
        else:
            serializer.save()

    @action(
        ["post"],
        detail=False,
        permission_classes=(IsAuthenticatedOrReadOnly,)
    )
    def set_password(self, request):
        user = self.request.user
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_password = request.data.get("new_password")
            current_password = request.data.get("current_password")
            if user.check_password(current_password):
                if new_password == current_password:
                    raise serializers.ValidationError(
                        {'new_password': 'Новый пароль должен отличаться от текущего.'}
                    )
                user.set_password(new_password)
                user.save()
                return Response({"status": "password set"})
            else:
                raise serializers.ValidationError(
                    {'current_password': 'Неправильный пароль.'}
                )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


# ----------end-users-------


# -----------start-news------


class NewsView(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = NewsFilter
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get_serializer_class(self):
        method = self.request.method
        if method == "POST" or method == "PATCH":
            return CreateNewsSerializers
        return ShowNewsSerializer if self.action == 'retrieve' \
            else ShowNewsListSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create_comment(self, request, pk=None, *args, **kwargs):
        blog_post = get_object_or_404(BlogPost, pk=pk)
        user = request.user
        serializer = CommentsSerializers(
            data=request.data)  # Предполагается, что данные комментария передаются через запрос
        if serializer.is_valid():
            serializer.save(blog_post=blog_post,
                            user=user)  # Предполагается, что метод save требует передачи blog_post и user
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ----------end-news--------
