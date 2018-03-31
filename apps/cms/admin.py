from django.contrib import admin

from apps.generic.admin import GenericModelAdmin
from apps.cms.models import (
    Feedback, Poll, PollItem
)


class PollItemInline(admin.TabularInline):
    model = PollItem


@admin.register(Poll)
class PollAdmin(GenericModelAdmin):
    inlines = (PollItemInline,)


@admin.register(Feedback)
class FeedbackAdmin(GenericModelAdmin):
    pass
