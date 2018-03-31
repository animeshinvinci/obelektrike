from django.contrib import admin

from apps.generic.admin import GenericModelAdmin
from apps.cms.models import (
    SeoPage, Feedback, Poll, PollItem
)


@admin.register(SeoPage)
class SeoPageInline(GenericModelAdmin):
    model = SeoPage
    list_display = (
        'url',
    )


class PollItemInline(admin.TabularInline):
    model = PollItem


@admin.register(Poll)
class PollAdmin(GenericModelAdmin):
    inlines = (PollItemInline,)
    list_display = (
        'question',
        'is_published',
    )
    list_editable = (
        'is_published',
    )


@admin.register(Feedback)
class FeedbackAdmin(GenericModelAdmin):
    pass
