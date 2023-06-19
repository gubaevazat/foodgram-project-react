import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from recipes.models import Ingredient, Recipe, RecipeIngredients, Tag
from users.serializers import UserSerializer


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
        # extra_kwargs = {
        #     'name': {'required': False},
        #     'color': {'required': False},
        #     'slug': {'required': False}
        # }


class RecipeIngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор модели RecipeIngredients."""
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(source='ingredient.measurement_unit')

    class Meta:
        fields = ('id', 'name', 'measurement_unit', 'amount')
        model = RecipeIngredients
        read_only_fields = ('name', 'measurement_unit')


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class RecipeSerializerGet(serializers.ModelSerializer):
    """Сериализатор модели Recipe для чтения."""
    tags = TagSerializer(many=True)
    author = UserSerializer(required=False)
    ingredients = RecipeIngredientsSerializer(
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

    def get_user(self):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return None
        return request.user

    def get_is_favorited(self, obj):
        user = self.get_user()
        if user is None:
            return False
        return user.favorites.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.get_user()
        if user is None:
            return False
        return user.in_shopping_cart.filter(recipe=obj).exists()


class RecipeSerializerPost(serializers.ModelSerializer):
    """Сериализатор модели Recipe для создания/обновления."""
    ingredients = RecipeIngredientsSerializerPost(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    image = Base64ImageField()
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        fields = ('author', 'ingredients', 'tags', 'image',
                  'name', 'text', 'cooking_time')
        model = Recipe

    def create(self, validated_data):
        print(validated_data)
        tags = validated_data.pop('tags')

        ingredients_list = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients_list:
            ingredient_id = ingredient.pop('ingredient')
            RecipeIngredients.objects.create(
                recipe=recipe,
                ingredient=Ingredient.objects.get(**ingredient_id),
                **ingredient
            )
        return recipe

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
