from django.contrib import admin

from apps.email.models import Email
from apps.generic.admin import GenericModelAdmin


@admin.register(Email)
class EmailAdmin(GenericModelAdmin):
    list_display = (
        'creation_date',
        'from_email',
        'to_emails',
        'subject',
    )
    search_fields = (
        'from_email',
        'to_emails',
        'subject',
        'body',
    )

    def has_add_permission(self, request):
        return False
