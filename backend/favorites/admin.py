from django.contrib import admin

from favorites.models import Favorite, ShoppingCart, Subscription
from users.mixins import StaffInAdminMixin


@admin.register(Favorite)
class FavoriteAdmin(StaffInAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    list_display_links = ('id', 'user', 'recipe')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(StaffInAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    list_display_links = ('id', 'user', 'recipe')


@admin.register(Subscription)
class SubscriptionAdmin(StaffInAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'user', 'subscription')
    list_display_links = ('id', 'user', 'subscription')
