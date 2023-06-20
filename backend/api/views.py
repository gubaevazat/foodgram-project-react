from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import serializers, viewsets
# from rest_framework.permissions import SAFE_METHODS
from rest_framework.decorators import action

from api.filters import IngredientFilter, RecipeFilter
from api.pagination import FoodgramPagination
from api.serializers import (FavoriteSerializer, IngredientSerializer,
                             RecipeSerializerGet, RecipeSerializerPost,
                             ShoppingCartSerializer, TagSerializer)
from recipes.models import Ingredient, Recipe, Tag


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
        if self.action in ['list', 'retrieve']:
            return RecipeSerializerGet
        elif self.action == 'favorite':
            return FavoriteSerializer
        elif self.action == 'shopping_cart':
            return ShoppingCartSerializer
        return RecipeSerializerPost

    @action(
        detail=True,
        methods=('post', 'delete'),
    )
    def favorite(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'DELETE':
            favorite = user.favorite_recipes.filter(recipe=recipe)
            if favorite:
                raise serializers.ValidationError(
                    'Рецепт отсутствует в избранном.'
                )
            favorite.delete()
        data = {'user': user.pk, 'recipe': pk}
        favorite = data

        return user
