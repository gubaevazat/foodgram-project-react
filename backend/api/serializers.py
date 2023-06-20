from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import Ingredient, Recipe, RecipeIngredients, Tag
from users.serializers import UserSerializer
from api.custom_fields import Base64ImageField
from favorites.models import Favorite, ShoppingCart, Subscription
from api.validators import IngredientsValidator


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор модели Ingredient"""

    class Meta:
        fields = '__all__'
        model = Ingredient


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор модели Tag."""

    class Meta:
        fields = '__all__'
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
    amount = serializers.IntegerField(min_value=1)


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
        exclude = ('pub_date',)
        model = Recipe
        validators = [IngredientsValidator()]

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients_list = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        for value in ingredients_list:
            ingredient = get_object_or_404(Ingredient, id=value.pop('id'))
            recipe.ingredients.add(
                ingredient,
                through_defaults=value
            )
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        instance.tags.set(tags)
        ingredients_list = validated_data.pop('ingredients')
        instance.ingredients.clear()
        for value in ingredients_list:
            ingredient = get_object_or_404(Ingredient, id=value.pop('id'))
            instance.ingredients.add(
                ingredient,
                through_defaults=value
            )
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeSerializerGet(instance, context=self.context).data


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Favorite."""

    class Meta:
        model = Favorite
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'recipe'),
                message='Рецепт есть в избранном! Добавлять можно один раз.'
            )
        ]


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для модели ShoppingCart."""

    class Meta:
        model = ShoppingCart
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('user', 'recipe'),
                message='Рецепт в корзине покупок! Добавлять можно один раз.'
            )
        ]
