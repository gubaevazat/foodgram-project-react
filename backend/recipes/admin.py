from django.contrib import admin

from recipes.models import Ingredient, Recipe, Tag, RecipeIngredients


class RecipeIngredientsInline(admin.TabularInline):
    model = RecipeIngredients
    extra = 1


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientsInline,)
