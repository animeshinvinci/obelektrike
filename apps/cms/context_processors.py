from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

from apps.cms.models import Material


def cms_context_processors(request):
    kwargs = {}
    materials = getattr(settings, 'MATERIALS', {})
    resolver_match = request.resolver_match
    for url_name in materials:
        if (resolver_match and url_name == resolver_match.url_name) or url_name == '*':
            for template_tag in materials[url_name]:
                pagetype = materials[url_name][template_tag]
                kwargs[template_tag] = Material.objects.filter(pagetype=pagetype).first()

    site = get_current_site(request)
    site_profile = site.get_profile()
    baseurl = request.build_absolute_uri(location='')

    kwargs['meta_title'] = u'%s | %s' % (site_profile.seo_title, site.name)
    kwargs['meta_keywords'] = site_profile.seo_keywords
    kwargs['meta_description'] = site_profile.seo_description
    kwargs['meta_author'] = site_profile.seo_author
    kwargs['meta_canonical'] = baseurl

    kwargs['meta_yandex_verification'] = site_profile.yandex_verification
    kwargs['meta_google_verification'] = site_profile.google_verification
    kwargs['meta_stat_yandex'] = site_profile.stat_yandex
    kwargs['meta_stat_google'] = site_profile.stat_google
    kwargs['meta_stat_liveinternet'] = site_profile.stat_liveinternet
    return kwargs
