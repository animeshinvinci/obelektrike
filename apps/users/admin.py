from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _ul

from apps.users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {
            'fields': (
                'avatar',
                'about',
                'city',
            )
        }),
        (_ul('Ключи'), {
            'fields': (
                'reset_password_key',
                'registration_key',
            )
        }),
        (_ul('Подписка'), {
            'fields': (
                'is_subscribe',
                'date_subscribe',
            )
        }),
    )
    readonly_fields = (
        'reset_password_key',
        'registration_key',
    )
    list_display = BaseUserAdmin.list_display + (
        'is_active',
        'is_subscribe',
    )
