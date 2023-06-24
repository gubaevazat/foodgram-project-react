from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.custom_fields import Base64ImageField
from api.validators import (AuthorUserValidator, IngredientsValidator,
                            ModelInstanceExistsValidator)
from favorites.models import Favorite, ShoppingCart, Subscription
from recipes.models import Ingredient, Recipe, RecipeIngredients, Tag
from users.serializers import UserSerializer

User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор модели Ingredient"""

    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор модели Tag."""

    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tag


class RecipeIngredientsSerializerGet(serializers.ModelSerializer):
    """Сериализатор ингредиентов рецепта для чтения."""
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        fields = ('id', 'name', 'measurement_unit', 'amount')
        model = RecipeIngredients


class RecipeIngredientsSerializerPost(serializers.Serializer):
    """Сериализатор ингредиентов рецепта для создания/обновления """
    id = serializers.IntegerField()
    amount = serializers.IntegerField(min_value=1, max_value=10000)


class RecipeSerializerGet(serializers.ModelSerializer):
    """Сериализатор модели Recipe для чтения."""
    tags = TagSerializer(many=True)
    author = UserSerializer(required=False)
    ingredients = RecipeIngredientsSerializerGet(
        source='recipeingredients_set',
        many=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')
        model = Recipe
        read_only_fields = fields

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        return (user.is_authenticated and user.favorite_recipes.filter(
            recipe=obj
        ).exists())

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        return (user.is_authenticated and user.in_shopping_cart_recipes.filter(
            recipe=obj
        ).exists())


class RecipeSerializerPost(serializers.ModelSerializer):
    """Сериализатор модели Recipe для создания/обновления."""
    ingredients = RecipeIngredientsSerializerPost(
        many=True
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    image = Base64ImageField()
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        fields = ('ingredients', 'tags', 'image', 'author',
                  'name', 'text', 'cooking_time')
        model = Recipe
        validators = [
            IngredientsValidator(),

        ]

    def create_ingredients(self, recipe, ingredients_list):
        for value in ingredients_list:
            ingredient = get_object_or_404(Ingredient, id=value.pop('id'))
            recipe.ingredients.add(
                ingredient,
                through_defaults=value
            )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients_list = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(recipe, ingredients_list)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        instance.tags.set(tags)
        ingredients_list = validated_data.pop('ingredients')
        instance.ingredients.clear()
        self.create_ingredients(instance, ingredients_list)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeSerializerGet(instance, context=self.context).data


class RecipeSmallSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = fields


class BaseFavoritesSerializator(serializers.ModelSerializer):
    """Базовый сериализатор для подписок/избранного/корзины"""
    def get_validators(self):
        validators = super().get_validators()
        if self.context['request'].method == 'POST':
            validators.append(UniqueTogetherValidator(
                queryset=self.Meta.model.objects.all(),
                fields=self.Meta.fields,
                message=(
                    'Экземпляр модели: '
                    f'{self.Meta.model._meta.verbose_name.capitalize()}'
                    ' существует. Добавлять можно один раз.'
                )
            ))
        elif self.context['request'].method == 'DELETE':
            validators.append(ModelInstanceExistsValidator(
                model=self.Meta.model,
                fields=self.Meta.fields,
            ))
        return validators

    def delete(self, data):
        self.Meta.model.objects.filter(**data).delete()


class FavoriteSerializer(BaseFavoritesSerializator):
    """Сериализатор для модели Favorite."""

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')


class ShoppingCartSerializer(BaseFavoritesSerializator):
    """Сериализатор для модели ShoppingCart."""

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')


class SubscriptionSerializer(BaseFavoritesSerializator):
    """Сериализатор для модели Subscription"""

    class Meta:
        model = Subscription
        fields = ('user', 'subscription')
        validators = [
            AuthorUserValidator(
                model=Subscription,
                fields=('user', 'subscription')
            )
        ]


class SubscriptionSerializerGet(serializers.ModelSerializer):
    """Сериализатор для возврата списка подписок."""
    recipes = serializers.SerializerMethodField()
    is_subscribed = serializers.BooleanField(default=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')
        read_only_fields = fields

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        recipes_limit = int(
            self.context['request'].query_params.get(
                'recipes_limit',
                settings.NUMBER_RECIPES_SUBSCRIPTIONS
            ))
        data = obj.recipes.all()[:recipes_limit]
        serializer = RecipeSmallSerializer(data, many=True)
        return serializer.data
