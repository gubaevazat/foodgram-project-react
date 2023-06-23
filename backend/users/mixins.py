class StaffInAdminMixin(object):
    """Для администраторов отображение моделей в админке."""

    def has_add_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True
