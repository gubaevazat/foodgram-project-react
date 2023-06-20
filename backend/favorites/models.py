from django.db import models
from django.contrib.auth import get_user_model

from recipes.models import Recipe

User = get_user_model()


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='подписчик'
    )
    subscription = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers',
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


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name='пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_users',
        verbose_name='рецепт',
    )

    class Meta:
        verbose_name = 'избранные рецепты'
        verbose_name_plural = 'избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='check_unique_user_favorite',
            ),
        ]


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='in_shopping_cart_recipes',
        verbose_name='пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_shopping_cart_users',
        verbose_name='рецепт',
    )

    class Meta:
        verbose_name = 'список покупок'
        verbose_name_plural = 'список покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='check_unique_user_shopping_cart',
            ),
        ]
