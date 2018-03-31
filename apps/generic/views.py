import os

from ckeditor_uploader.views import ImageUploadView as CKImageUploadView
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.sitemaps import Sitemap as BaseSitemap
from django.contrib.sitemaps.views import sitemap
from django.contrib.syndication.views import Feed
from django.core.cache import cache
from django.http import JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from PIL import Image

from apps.blogs.models import Category, Post


class RobotTemplateView(TemplateView):
    content_type = 'text/plain'

    def get_template_names(self):
        if settings.DEBUG:
            return ('robots-disallow.txt',)
        return ('robots.txt',)


class SiteMap(BaseSitemap):
    url_type = None

    def get_urls(self, page=1, site=None, protocol=None):
        urls = super(SiteMap, self).get_urls(page=page, site=site, protocol=protocol)
        for url in urls:
            url['type'] = self.url_type
        return urls


class StaticViewSitemap(SiteMap):
    changefreq = 'daily'
    priority = 0.7
    url_type = 'static'

    def items(self):
        return ['index']

    def location(self, item):
        return reverse(item)


class BlogsPostsSitemap(SiteMap):
    changefreq = "daily"
    priority = 0.6
    url_type = 'post'

    def items(self):
        return Post.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.modification_date

    def location(self, obj):
        return reverse('posts-category-detail', kwargs={'slug': obj.slug})


class BlogsCategoriesSitemap(SiteMap):
    changefreq = "daily"
    priority = 0.7
    url_type = 'category'

    def items(self):
        return Category.objects.filter(is_published=True)

    def lastmod(self, obj):
        try:
            return Post.objects.filter(is_published=True, category=obj).latest("modification_date").modification_date
        except Post.DoesNotExist:
            return None

    def location(self, obj):
        return reverse('posts-category-list', kwargs={'category_slug': obj.slug})


def sitemap_xml(request, *args, **kwargs):
    sitemaps = {
        'static': StaticViewSitemap,
        'posts': BlogsPostsSitemap,
        'categories': BlogsCategoriesSitemap,
    }
    kwargs['sitemaps'] = sitemaps
    return sitemap(request, *args, **kwargs)


def sitemap_html(request, *args, **kwargs):
    sitemaps = {
        'static': StaticViewSitemap,
        'posts': BlogsPostsSitemap,
        'categories': BlogsCategoriesSitemap,
    }
    kwargs['sitemaps'] = sitemaps
    kwargs['template_name'] = 'sitemap.html'
    kwargs['content_type'] = None
    return sitemap(request, *args, **kwargs)


class BlogsFeed(Feed):
    title = ""
    link = ""
    description = ""

    def items(self):
        return Post.objects.filter(is_published=True)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.announcement

    def item_link(self, item):
        return reverse('posts-category-detail', kwargs={'slug': item.slug})


def feed(request):
    feed = BlogsFeed()
    return feed(request)


@staff_member_required
def flush_cache(request):
    cache.clear()
    return JsonResponse({'result': 'success'})


class ImageUploadView(CKImageUploadView):

    @staticmethod
    def _save_file(request, uploaded_file):
        saved_path = CKImageUploadView._save_file(request, uploaded_file)
        full_saved_path = os.path.join(settings.MEDIA_ROOT, saved_path)
        with open(full_saved_path, 'r+b') as f:
            with Image.open(f) as image:
                image.thumbnail((800, 600), Image.ANTIALIAS)
                image.save(full_saved_path, quality=70)
        return saved_path

    @method_decorator(staff_member_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ImageUploadView, self).dispatch(*args, **kwargs)
