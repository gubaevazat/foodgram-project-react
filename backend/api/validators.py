from rest_framework.serializers import ValidationError


class ModelInstanceExistsValidator:
    """Валидатор проверки существования экземпляра модели."""

    def __init__(self, model, fields):
        self.model = model
        self.fields = fields

    def __call__(self, data: dict):
        validated_data = {}
        for field in self.fields:
            if field not in data:
                raise ValidationError(
                    'Недопустимое имя поля или оно отсутсвует.'
                )
            validated_data[field] = data[field]
            queryset = self.model.objects.filter(**validated_data).exists()
            if not queryset:
                raise ValidationError(
                    'Экземпляра модели: '
                    f'{self.model._meta.verbose_name.capitalize()}'
                    ' не существует.'
                )


class AuthorUserValidator(ModelInstanceExistsValidator):
    """Валидация что автор не может подписаться сам на себя."""
    def __call__(self, data: dict):
        if data[self.fields[0]] == data[self.fields[1]]:
            raise ValidationError(
                'Пользователь не может подписаться на самого себя!'
            )


class IngredientsValidator:
    """Валидатор ингредиентов при записи/обновлении."""
    def __call__(self, value):
        ingredients_id = [id['id'] for id in value.get('ingredients')]
        if len(set(ingredients_id)) != len(ingredients_id):
            raise ValidationError(
                'У рецепта не может быть одинаковых ингредиентов.'
            )
