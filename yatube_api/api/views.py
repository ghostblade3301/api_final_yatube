from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from posts.models import Follow, Group, Post
from . import serializers
from .permissions import IsAuthorOrReadOnly

User = get_user_model()


# Класс для обработки запросов к модели "Post"
class PostViewSet(viewsets.ModelViewSet):
    # Указываем, какой сериализатор использовать для этой модели
    serializer_class = serializers.PostSerializer
    # Устанавливаем права доступа для "Post"
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,)
    # Устанавливаем набор записей, с которыми работаем
    queryset = Post.objects.all()
    # Устанавливаем класс пагинации
    pagination_class = LimitOffsetPagination

    # Переопределяем метод, который вызывается при создании новой записи
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# Класс для обработки запросов к модели "Group"
class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    # Указываем, какой сериализатор использовать для этой модели
    serializer_class = serializers.GroupSerializer
    # Устанавливаем права доступа для "Group"
    permission_classes = (permissions.AllowAny,)
    # Устанавливаем набор записей, с которыми работаем
    queryset = Group.objects.all()


# Класс для обработки запросов к модели "Comment"
class CommentViewSet(viewsets.ModelViewSet):
    # Указываем, какой сериализатор использовать для этой модели
    serializer_class = serializers.CommentSerializer
    # Устанавливаем права доступа для "Comment"
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,)

    # Переопределяем метод, который возвращает набор
    # записей (комментариев) для конкретного поста
    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        return post.comments.all()

    # Переопределяем метод, который вызывается
    # при создании нового объекта (комментария)
    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post_id=self.kwargs.get('post_id')
        )


# Класс для обработки запросов к модели "Follow"
class FollowView(generics.ListCreateAPIView):
    # Указываем, какой сериализатор использовать для этой модели
    serializer_class = serializers.FollowSerializer
    # Устанавливаем права доступа для "Follow"
    permission_classes = (permissions.IsAuthenticated,)
    # Устанавливаем методы фильтрации
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    # Переопределяем метод, который возвращает
    # набор записей (Follow-объектов), связанных с текущим пользователем
    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    # Переопределяем метод, который вызывается
    # при создании нового объекта (Follow-объекта)
    def perform_create(self, serializer):
        following_user = get_object_or_404(
            User,
            username=self.request.data.get('following')
        )
        serializer.save(
            user=self.request.user,
            following=following_user
        )
