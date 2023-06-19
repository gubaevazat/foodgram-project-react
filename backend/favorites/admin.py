from django.contrib import admin

from favorites.models import Favorite, ShoppingCart, Subscription


admin.register(Favorite)
admin.register(ShoppingCart)
admin.register(Subscription)
