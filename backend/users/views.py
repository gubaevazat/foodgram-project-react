from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.pagination import FoodgramPagination
from api.serializers import SubscriptionSerializer, SubscriptionSerializerGet

User = get_user_model()


class UserViewSet(DjoserUserViewSet):
    """Вьюсет для подписок."""

    http_method_names = ('get', 'post', 'delete')
    pagination_class = FoodgramPagination

    def get_serializer_class(self):
        if self.action == 'subscribe':
            return SubscriptionSerializer
        elif self.action == 'subscriptions':
            return SubscriptionSerializerGet
        return super().get_serializer_class()

    @action(
        detail=True,
        methods=('delete', 'post'),
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, id):
        user = self.get_instance()
        subscription = get_object_or_404(User, pk=id)
        data = {'user': user.pk, 'subscription': id}
        if request.method == 'DELETE':
            subscribe = self.get_serializer(data=data)
            subscribe.is_valid(raise_exception=True)
            subscribe.delete(data)
            return Response(status=status.HTTP_204_NO_CONTENT)
        subscribe = self.get_serializer(data=data)
        subscribe.is_valid(raise_exception=True)
        subscribe.save()
        serializer = SubscriptionSerializerGet(
            subscription,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        user = self.get_instance()
        paginated_subscriptions = self.paginate_queryset(
            User.objects.filter(subscribers__user=user).order_by('id')
        )
        serializer = self.get_serializer(
            paginated_subscriptions, many=True
        )
        return self.get_paginated_response(serializer.data)
