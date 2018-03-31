from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site

from apps.blogs.models import Category
from apps.users.forms import SubscribeForm


def main_context_processors(request):
    kwargs = {}

    kwargs['site'] = get_current_site(request)
    kwargs['site_profile'] = kwargs['site'].get_profile()
    kwargs['host'] = "http://" + kwargs['site'].domain
    kwargs['page_path'] = kwargs['host'] + request.path

    if kwargs['site_profile'].important_message:
        messages.success(request, kwargs['site_profile'].important_message, extra_tags='important')

    kwargs['subscribe_form'] = SubscribeForm()
    kwargs['categories'] = Category.objects.filter(is_published=True, categorytype=Category.CATEGORY_NONE)
    return kwargs
