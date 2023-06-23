from django.contrib import admin

from recipes.models import Ingredient, Recipe, RecipeIngredients, Tag
from users.mixins import StaffInAdminMixin


class RecipeIngredientsInline(StaffInAdminMixin, admin.TabularInline):
    model = RecipeIngredients
    extra = 1
    fields = ('ingredient', 'amount', 'measurement_unit')
    readonly_fields = ('measurement_unit',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('ingredient')

    @admin.display(description='еденица измерения')
    def measurement_unit(self, obj):
        return obj.ingredient.measurement_unit


@admin.register(Ingredient)
class IngredientAdmin(StaffInAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_display_links = ('id', 'name')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(StaffInAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    list_display_links = ('id', 'name')


@admin.register(Recipe)
class RecipeAdmin(StaffInAdminMixin, admin.ModelAdmin):
    inlines = (RecipeIngredientsInline,)
    list_display = ('id', 'name', 'author', 'favorite_count')
    list_display_links = ('id', 'name')
    list_filter = ('name', 'author', 'tags')
    search_fields = ('name', 'author')
    readonly_fields = ('favorite_count',)

    @admin.display(description='счётчик избранного')
    def favorite_count(self, instance):
        return instance.favorite_users.count()
