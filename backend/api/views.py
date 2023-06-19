from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS

from api.filters import IngredientFilter, RecipeFilter
from api.pagination import FoodgramPagination
from api.serializers import (IngredientSerializer, RecipeSerializerGet,
                             RecipeSerializerPost, TagSerializer)
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
    queryset = Recipe.objects.all()
    pagination_class = FoodgramPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeSerializerGet
        return RecipeSerializerPost
