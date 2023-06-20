from django_filters import rest_framework as filters

from recipes.models import Ingredient, Recipe


class IngredientFilter(filters.FilterSet):
    """Фильтр поиска по ингридентам."""
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(filters.FilterSet):
    """Фильтр поиска по рецептам."""
    author = filters.NumberFilter(field_name='author__id')
    tags = filters.CharFilter(field_name='tags__slug')
    is_favorited = filters.BooleanFilter(
        field_name='favorite_users__user',
        method='get_favorites'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='in_shopping_cart_users__user',
        method='get_favorites'
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')

    def get_favorites(self, queryset, field_name, value):
        """Возвращает объекты из корзины/избранного для пользователя."""
        user = self.request.user
        if not user.is_authenticated:
            return queryset
        if value:
            queryset = queryset.filter(**{field_name: user})
        else:
            queryset = queryset.exclude(**{field_name: user})
        return queryset
