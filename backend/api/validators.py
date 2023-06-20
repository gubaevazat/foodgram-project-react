from rest_framework.serializers import ValidationError


class ModelInstanceExistsValidator:
    """Валидатор проверки существования экземпляра модели."""

    def __init__(self, model, fields, request_method=None):
        self.model = model
        self.fields = fields
        self.request_method = request_method

    def __call__(self, data: dict):
        if not self.request_method == 'delete':
            return
        validated_data = {}
        for field in self.fields:
            if field not in data:
                raise ValidationError(
                    'Недопустимое имя поля или оно отсутсвует.'
                )
            validated_data[field] = data[field]
            queryset = self.model.objects.filter(**validated_data)
            if not queryset.exists():
                raise ValidationError(
                    f'Экземпляра модели {self.model} не существует.'
                )


class IngredientsValidator:
    """Валидатор ингредиентов при записи/обновлении."""
    def __call__(self, value):
        ingredients_id = [id['id'] for id in value.get('ingredients')]
        if len(set(ingredients_id)) != len(ingredients_id):
            raise ValidationError(
                'У рецепта не может быть одинаковых ингредиентов.'
            )
