from rest_framework import serializers as drf_serializers
from django.contrib.auth import get_user_model
from djoser import serializers

User = get_user_model()


class UserSerializer(serializers.UserSerializer):
    """Сериализатор модели User."""

    is_subscribed = drf_serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return request.user.subscriptions.filter(subscription=obj).exists()


class CreateUserSerializer(serializers.UserCreateSerializer):
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
