from django.db import models
from django.contrib.auth import get_user_model

from recipes.models import Recipe

User = get_user_model()


class FavoritesBase(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='пользователь'
    )

    class Meta:
        abstract = True


class Subscription(FavoritesBase):
    subscription = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='подписка на автора',
    )

    class Meta:
        verbose_name = 'подписка на автора'
        verbose_name_plural = 'подписки на авторов'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'subscription'],
                name='check_unique_user_subscription',
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('subscription')),
                name='check_not_equal_user_subscription',
            ),
        ]


class Favorite(FavoritesBase):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='рецепт',
    )

    class Meta:
        default_related_name = 'favorites'
        verbose_name = 'избранные рецепты'
        verbose_name_plural = 'избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='check_unique_user_favorite',
            ),
        ]


class ShoppingCart(FavoritesBase):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='рецепт',
    )

    class Meta:
        default_related_name = 'in_shopping_cart'
        verbose_name = 'список покупок'
        verbose_name_plural = 'список покупок'
