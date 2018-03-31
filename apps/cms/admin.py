from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.sites.models import Site

from apps.cms.models import (
    Feedback, Material, PollItem, PollMaterial, PostMaterial, SiteProfile,
    TextMaterial,
)
from apps.generic.admin import GenericModelAdmin


@admin.register(Material)
class MaterialAdmin(GenericModelAdmin):

    def formfield_for_dbfield(self, db_field, request, *args, **kwargs):
        formfield = super(MaterialAdmin, self).formfield_for_dbfield(db_field, request, *args, **kwargs)
        if db_field.name == 'data' and request.resolver_match.args:
            if Material.objects.filter(
                id=request.resolver_match.args[0],
                pagetype__in=getattr(settings, 'MATERIAL_TYPES_WITHOUT_WYSIWYG', ())
            ).exists():
                formfield.widget = forms.Textarea()
        return formfield


@admin.register(PostMaterial)
class PostMaterialAdmin(GenericModelAdmin):
    pass


@admin.register(TextMaterial)
class TextMaterialAdmin(GenericModelAdmin):
    pass


class PollItemInline(admin.TabularInline):
    model = PollItem


@admin.register(PollMaterial)
class PollMaterialAdmin(GenericModelAdmin):
    inlines = (PollItemInline,)


@admin.register(Feedback)
class FeedbackAdmin(GenericModelAdmin):
    pass


class SiteProfileInline(admin.StackedInline):
    model = SiteProfile


class SiteAdmin(admin.ModelAdmin):
    inlines = (
        SiteProfileInline,
    )


admin.site.unregister(Site)
admin.site.register(Site, SiteAdmin)
