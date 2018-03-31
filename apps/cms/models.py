import random

from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import F, Max
from django.utils.translation import ugettext_lazy as _ul

from apps.blogs.models import Category, Post, Tag
from apps.generic.models import GenericDateModel


class Material(GenericDateModel):
    pagetype = models.PositiveSmallIntegerField(
        verbose_name=_ul('Тип страницы'),
        unique=True,
        choices=getattr(settings, 'MATERIAL_TYPES')
    )
    title = models.CharField(verbose_name=_ul('Заголовок'), max_length=255)
    data = RichTextUploadingField(verbose_name=_ul('Контент'), default="")

    def posts(self):
        post_material = PostMaterial.objects.filter(material=self).first()
        if post_material is not None:
            qs = Post.objects.filter(is_published=True).exclude(category__categorytype=Category.CATEGORY_QUESTIONS)
            filter_catgories = list(post_material.filter_catgories.all())
            if filter_catgories:
                qs = Post.objects.filter(is_published=True)
                qs = qs.filter(category__in=filter_catgories)
            filter_tags = list(post_material.filter_tags.all())
            if filter_tags:
                qs = qs.filter(tags__in=filter_tags)
            if post_material.sort_publication_date:
                qs = qs.order_by('-publication_date')
            if post_material.sort_comments_count:
                qs = qs.filter(comment__isnull=False).annotate(max_comment_creationdate=Max('comment__creation_date'))
                qs = qs.order_by('-max_comment_creationdate')
            if post_material.sort_views_count:
                qs = qs.order_by('-view_count')
            return qs[:post_material.count]
        return []

    def text(self):
        text_material = TextMaterial.objects.filter(material=self).first()
        if text_material is not None:
            materials = self.data.split(text_material.separator)
            if text_material.is_random_show:
                return random.choice(materials)
            if text_material.is_day_show:
                # TODO
                return random.choice(materials)
        return self.data

    def poll(self):
        return PollMaterial.objects.filter(material=self).first()

    class Meta:
        verbose_name = _ul('Материал')
        verbose_name_plural = _ul('Материалы')

    def __str__(self):
        return u'%s' % self.title


class PostMaterial(GenericDateModel):
    material = models.OneToOneField(Material, verbose_name=_ul('Материал'), on_delete=models.CASCADE)
    filter_catgories = models.ManyToManyField(Category, verbose_name=_ul('Фильтровать по категориям'), blank=True)
    filter_tags = models.ManyToManyField(Tag, verbose_name=_ul('Фильтровать по меткам'), blank=True)
    sort_publication_date = models.BooleanField(verbose_name=_ul('Сортировать по дате публикации'), default=True)
    sort_comments_count = models.BooleanField(verbose_name=_ul('Сортировать по кол-ву комментариев'), default=False)
    sort_views_count = models.BooleanField(verbose_name=_ul('Сортировать по кол-ву просмотров'), default=False)
    count = models.PositiveIntegerField(verbose_name=_ul('Кол-во статей'), default=10)

    class Meta:
        verbose_name = _ul('Материал поста')
        verbose_name_plural = _ul('Материалы постов')

    def __str__(self):
        return u'%s' % self.material.title


class TextMaterial(GenericDateModel):
    material = models.OneToOneField(Material, verbose_name=_ul('Материал'), on_delete=models.CASCADE)
    is_random_show = models.BooleanField(verbose_name=_ul('Показывать рандомно'), default=True)
    is_day_show = models.BooleanField(verbose_name=_ul('Показывать рандомно по дням'), default=False)
    separator = models.CharField(verbose_name=_ul('Разделитель'), max_length=255, default='<cut/>')

    class Meta:
        verbose_name = _ul('Материал текста')
        verbose_name_plural = _ul('Материалы текстов')

    def __str__(self):
        return u'%s' % self.material.title


class PollMaterial(GenericDateModel):
    material = models.OneToOneField(Material, verbose_name=_ul('Материал'), on_delete=models.CASCADE)
    question = models.CharField(verbose_name=_ul('Вопрос'), max_length=255)

    class Meta:
        verbose_name = _ul('Материал опроса')
        verbose_name_plural = _ul('Материалы опросов')

    def __str__(self):
        return u'%s' % self.material.title


class PollItem(GenericDateModel):
    poll = models.ForeignKey(PollMaterial, verbose_name=_ul('Опрос'), related_name="items", on_delete=models.CASCADE)
    rate = models.IntegerField(verbose_name=_ul('Кол-во за'), default=0)
    answer = models.CharField(verbose_name=_ul('Ответ'), max_length=255)

    @property
    def rate_percentage(self):
        total = sum(self.__class__.objects.filter(poll=self.poll).values_list('rate', flat=True))
        if total:
            return int(float(self.rate * 100) / float(total))
        return 0

    def vote_action(self, session):
        if self.poll.has_session_key(session, 'pollitem_vote', setup=True):
            return
        self.__class__.objects.filter(id=self.id).update(rate=F('rate') + 1)

    class Meta:
        verbose_name = _ul('Ответ')
        verbose_name_plural = _ul('Ответы')

    def __str__(self):
        return u'%s' % self.answer


class Feedback(GenericDateModel):
    name = models.CharField(verbose_name=_ul('Ваше имя'), max_length=255)
    email = models.EmailField(verbose_name=_ul('Контактный email'), max_length=255)
    message = RichTextUploadingField(verbose_name=_ul('Сообщение'), config_name='feedback')

    class Meta:
        verbose_name = _ul('Обратная связь')
        verbose_name_plural = _ul('Обратная связь')

    def __str__(self):
        return u'%s - %s' % (self.creation_date, self.name)


def get_profile(self):
    try:
        return self.profile
    except Exception:
        return SiteProfile.objects.create(site=self)


Site.add_to_class('get_profile', get_profile)


class SiteProfile(GenericDateModel):
    site = models.OneToOneField(Site, related_name='profile', on_delete=models.CASCADE)

    description = models.CharField(max_length=255, null=True, blank=True)
    seo_title = models.CharField(max_length=255, null=True, blank=True)
    seo_keywords = models.CharField(max_length=255, null=True, blank=True)
    seo_description = models.CharField(max_length=255, null=True, blank=True)
    seo_author = models.CharField(max_length=255, null=True, blank=True)
    stat_liveinternet = models.TextField(null=True, blank=True)
    stat_yandex = models.TextField(null=True, blank=True)
    stat_google = models.TextField(null=True, blank=True)
    yandex_verification = models.CharField(max_length=255, null=True, blank=True)
    google_verification = models.CharField(max_length=255, null=True, blank=True)
    important_message = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = _ul('Профайл сайта')
        verbose_name_plural = _ul('Профайлы сайтов')

    def __str__(self):
        return u"%s" % self.site
