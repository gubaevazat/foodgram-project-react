from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models


User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name='название',
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='название',
    )

    class Meta:
        verbose_name = 'ингридиент'
        verbose_name_plural = 'ингридиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):

    COLOR_PALETTE = [
        ('#FF0000', 'red', ),
        ('#FFFF00', 'yellow', ),
        ('#00FF00', 'lime'),
        ('#0000FF', 'blue'),
    ]

    name = models.CharField(
        max_length=200,
        verbose_name='название',
    )
    color = ColorField(samples=COLOR_PALETTE)
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='идентификатор'
    )

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'тэги'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='автор',
    )
    tags = models.ManyToManyField(Tag)
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredients'
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name='фото',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='название',
    )
    text = models.TextField(verbose_name='описание рецепта')
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='дата публикации'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'
        default_related_name = 'recipes'


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(verbose_name='количество')
