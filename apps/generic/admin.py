from django.contrib import admin
from django.utils.safestring import mark_safe


class GenericModelAdmin(admin.ModelAdmin):

    @staticmethod
    def site_url(obj):
        url = obj.get_absolute_url()
        if url:
            return mark_safe(u'<a href="%s">на сайте</a>' % url)
