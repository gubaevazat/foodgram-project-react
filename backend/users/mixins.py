from django.contrib.auth import get_user_model

User = get_user_model()


class StaffInAdminMixin(object):
    """Для администраторов отображение моделей и права  в админке."""

    def check_perm(self, request, obj=None):
        return obj is not None and isinstance(obj, User) and (
            obj.is_superuser or obj.is_staff)

    def has_add_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return (not self.check_perm(request, obj) or request.user == obj
                or request.user.is_superuser)

    def has_delete_permission(self, request, obj=None):
        return not self.check_perm(request, obj) or request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True
