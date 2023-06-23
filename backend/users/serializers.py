from django.contrib.auth import get_user_model
from djoser import serializers as djoser_serializers
from rest_framework import serializers as serializers

User = get_user_model()


class UserSerializer(djoser_serializers.UserSerializer):
    """Сериализатор модели User."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return (user.is_authenticated and user.subscriptions.filter(
            subscription=obj
        ).exists())


class CreateUserSerializer(djoser_serializers.UserCreateSerializer):
    """Сериализатор создания пользователя."""

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )
        read_only_fields = ('id',)
