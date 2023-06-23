from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    """Даёт доступ только автору."""

    message = 'Данный запрос недоступен для вас.'

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author
