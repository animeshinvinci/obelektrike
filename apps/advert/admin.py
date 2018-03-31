from django.contrib import admin

from apps.advert.models import Advert, Partner
from apps.generic.admin import GenericModelAdmin


@admin.register(Advert)
class AdvertAdmin(GenericModelAdmin):
    pass


@admin.register(Partner)
class PartnerAdmin(GenericModelAdmin):
    pass
