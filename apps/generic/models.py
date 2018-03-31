from django.db import models
from django.utils.translation import ugettext_lazy as _ul


class GenericDateModel(models.Model):
    creation_date = models.DateTimeField(
        verbose_name=_ul('Дата создания'),
        auto_now_add=True)
    modification_date = models.DateTimeField(
        verbose_name=_ul('Дата изменения'),
        auto_now=True)

    def has_session_key(self, session, key, setup=False):
        key = key + '_%s' % self.id
        result = session.get(key, False)
        if setup:
            session[key] = True
        return result

    class Meta:
        abstract = True


class GenericSeoModel(GenericDateModel):
    slug = models.SlugField(
        verbose_name=_ul('Слаг'),
        unique=True,
        max_length=255)

    seo_title = models.CharField(
        verbose_name=_ul('Заголовок (meta тег)'),
        max_length=255,
        null=True,
        blank=True)
    seo_keywords = models.CharField(
        verbose_name=_ul('Ключевые слова (meta тег)'),
        max_length=255,
        null=True,
        blank=True)
    seo_description = models.CharField(
        verbose_name=_ul('Описание (meta тег)'),
        max_length=255,
        null=True,
        blank=True)
    seo_author = models.CharField(
        verbose_name=_ul('Автор (meta тег)'),
        max_length=255,
        null=True,
        blank=True)

    is_published = models.BooleanField(
        verbose_name=_ul('Опубликован?'),
        default=True,
        db_index=True)

    class Meta:
        abstract = True
