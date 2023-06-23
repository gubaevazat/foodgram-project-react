from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from users.mixins import StaffInAdminMixin

User = get_user_model()


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        fields = ('username', 'email', 'first_name', 'last_name')


@admin.register(User)
class CustomUserAdmin(StaffInAdminMixin, admin.ModelAdmin):
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'username', 'first_name',
                           'last_name', 'password1', 'password2'),
            }
        ),
    )

    form = CustomUserChangeForm
    list_display = (
        'id',
        'email',
        'username',
        'first_name',
        'last_name',
        'is_active'
    )
    list_display_links = ('id', 'email', 'username')
    list_editable = ('is_active',)
    list_filter = ('email', 'first_name')
    search_fields = ('email', 'username', 'first_name', 'last_name')

    def get_fieldsets(self, request, obj=None):
        fields = ('is_active', 'is_staff', 'is_superuser')
        user = request.user
        if not obj:
            return self.add_fieldsets
        if user.is_staff and not user.is_superuser:
            fields = ('is_active',)
        return [
            (None, {'fields': ('email', 'password')}),
            (_('Personal info'), {'fields': ('first_name', 'last_name')}),
            (_('Permissions'), {'fields': fields}),
            (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        ]


admin.site.unregister(Group)
admin.site.site_header = 'Управление сайтом Foodgramm'
