from rest_framework import serializers as serializers
from django.contrib.auth import get_user_model
from djoser import serializers as djoser_serializers


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


# class SubscriptionSerializer(serializers.ModelSerializer):
#     """Сериализатор для модели Subscription"""

#     class Meta:
#         model = Subscription
#         fields = ('user', 'subscription')
#         validators = [
#             AuthorUserValidator(
#                 model=Subscription,
#                 fields=('user', 'subscription')
#             )
#         ]

#     def get_validators(self):
#         validators = super().get_validators()
#         if self.context['request'].method == 'POST':
#             validators.append(UniqueTogetherValidator(
#                 queryset=Subscription.objects.all(),
#                 fields=self.Meta.fields,
#                 message=(
#                     'Экземпляр модели: '
#                     f'{Subscription._meta.verbose_name.capitalize()}'
#                     ' существует. Добавлять можно один раз.'
#                 )
#             ))
#         elif self.context['request'].method == 'DELETE':
#             validators.append(ModelInstanceExistsValidator(
#                 model=Subscription,
#                 fields=('user', 'subscription')
#             ))
#         return validators

#     def delete(self, data):
#         Subscription.objects.filter(**data).delete()
