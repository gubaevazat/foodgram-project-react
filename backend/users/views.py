from api.serializers import SubscriptionSerializerGet, SubscriptionSerializer
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class UserViewSet(DjoserUserViewSet):
    """Вьюсет для подписок унаследован от djoser ViewSet."""

    @action(
        detail=True,
        methods=('delete', 'post')
    )
    def subscribe(self, request, id):
        user = request.user
        print(user)
        subscription = get_object_or_404(User, pk=id)
        print(subscription)
        data = {'user': user.pk, 'subscription': id}
        if request.method == 'DELETE':
            subscribe = SubscriptionSerializer(
                data=data,
                context={'request': request}
            )
            subscribe.is_valid(raise_exception=True)
            subscribe.delete(data)
            return Response(status=status.HTTP_204_NO_CONTENT)
        subscribe = SubscriptionSerializer(
            data=data,
            context={'request': request}
        )
        subscribe.is_valid(raise_exception=True)
        subscribe.save()
        serializer = SubscriptionSerializerGet(subscription)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
