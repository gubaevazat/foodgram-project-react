from django.db.models import Sum
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.filters import IngredientFilter, RecipeFilter
from api.pagination import FoodgramPagination
from api.permissions import IsAuthor
from api.serializers import (FavoriteSerializer, IngredientSerializer,
                             RecipeSerializerGet, RecipeSerializerPost,
                             RecipeSmallSerializer, ShoppingCartSerializer,
                             TagSerializer)
from recipes.models import Ingredient, Recipe, RecipeIngredients, Tag


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для модели Ingredient"""
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = IngredientFilter


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для модели Tag"""
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Tag"""
    http_method_names = ('get', 'post', 'patch', 'delete')
    queryset = Recipe.objects.all()
    pagination_class = FoodgramPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeSerializerGet
        elif self.action == 'favorite':
            return FavoriteSerializer
        elif self.action == 'shopping_cart':
            return ShoppingCartSerializer
        return RecipeSerializerPost

    def get_permissions(self):
        if self.action in ('favorite', 'shopping_cart',
                           'download_shopping_cart'):
            self.permission_classes = (IsAuthenticated,)
        elif self.action in ('partial_update', 'destroy'):
            self.permission_classes = (IsAuthor,)
        return super().get_permissions()

    def favorite_shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        data = {'user': user.pk, 'recipe': pk}
        if request.method == 'DELETE':
            favorite = self.get_serializer(data=data)
            favorite.is_valid(raise_exception=True)
            favorite.delete(data)
            return Response(status=status.HTTP_204_NO_CONTENT)
        favorite = self.get_serializer(data=data)
        favorite.is_valid(raise_exception=True)
        favorite.save()
        serializer = RecipeSmallSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=('post', 'delete')
    )
    def favorite(self, request, pk=None):
        return self.favorite_shopping_cart(request, pk)

    @action(
        detail=True,
        methods=('post', 'delete')
    )
    def shopping_cart(self, request, pk=None):
        return self.favorite_shopping_cart(request, pk)

    @action(
        detail=False,
        methods=('get',)
    )
    def download_shopping_cart(self, request):
        user = request.user
        ingredients = RecipeIngredients.objects.filter(
            recipe__in_shopping_cart_users__user=user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(
            amount_total=Sum('amount')
        ).order_by('-amount_total')
        ingredient_template = '{}, количество-{} {}'
        shopping_list = 'Список покупок: \n\n'
        shopping_list += '\n'.join(
            [
                ingredient_template.format(
                    ingredient['ingredient__name'],
                    ingredient['amount_total'],
                    ingredient['ingredient__measurement_unit']
                ) for ingredient in ingredients
            ])
        return HttpResponse(shopping_list, headers={
            'Content-Type': 'text/plain',
            'Content-Disposition': 'attachment; filename="shopping_list.txt"',
        })
