from django.conf import settings

from apps.blogs.models import Category, Post
from apps.users.forms import SubscribeForm
from apps.cms.models import SeoPage, Poll
from apps.advert.models import Advert


def main_context_processors(request):
    kwargs = {}
    post_qs = Post.objects.filter(
        is_published=True
    )
    kwargs['DEBUG'] = settings.DEBUG
    kwargs['absolute_url'] = request.build_absolute_uri(location='')
    kwargs['domain'] = request.build_absolute_uri('/')[:-1]
    kwargs['seo_page'] = SeoPage.objects.filter(url=request.path).first()
    kwargs['categories'] = Category.objects.filter(is_published=True, categorytype=Category.CATEGORY_NONE)
    kwargs['subscribe_form'] = SubscribeForm()
    kwargs['comment_posts'] = post_qs.exclude(
        category__categorytype=Category.CATEGORY_QUESTIONS
    ).filter(num_comments__gte=1).order_by('-modification_date', '-num_comments')[:5]
    kwargs['poll'] = Poll.objects.filter(is_published=True).first()
    kwargs['question_posts'] = post_qs.filter(
        category__categorytype=Category.CATEGORY_QUESTIONS
    ).order_by('-modification_date')[:5]

    for advert in Advert.objects.all():
        kwargs[advert.key] = advert.content
    return kwargs
