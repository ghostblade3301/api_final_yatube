from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from posts.models import Comment, Follow, Group, Post
from rest_framework import serializers


# Сериализатор для модели Post
class PostSerializer(serializers.ModelSerializer):
    # Указываем, что поле author должно быть только для чтения
    # и связано с моделью пользователя через SlugRelatedField
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Post
        fields = '__all__'


# Cериализатор для модели Comment
class CommentSerializer(serializers.ModelSerializer):
    # Указываем, что поле author должно быть только для чтения
    # и связано с моделью пользователя через SlugRelatedField
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author', 'post')


# Cериализатор для модели Group
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


# Cериализатор для модели Follow
class FollowSerializer(serializers.ModelSerializer):
    # Указываем, что поле user должно быть только для чтения и связано
    # с моделью пользователя через SlugRelatedField
    # с CurrentUserDefault значением по умолчанию
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    # Указываем, что поле following должно быть связано с моделью пользователя
    # через SlugRelatedField и содержать все объекты из таблицы пользователя
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=get_user_model().objects.all(),
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')
        # Указываем валидатор, проверяющий уникальность комбинации
        # полей user и following в таблице Follow
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message=_('You already followed this author'),
            ),
        ]

    # Проверяем, что пользователь не пытается подписаться на самого себя
    def validate(self, data):
        user = self.context['request'].user
        following = data['following']
        if user == following:
            raise serializers.ValidationError(
                _("You can't follow yourself."))
        return data
