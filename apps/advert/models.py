from django.db import models
from django.utils.translation import ugettext_lazy as _ul


class Partner(models.Model):
    name = models.CharField(
        verbose_name=_ul('Партнерка'),
        max_length=255,
        help_text=_ul('Название партнерки'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _ul('Партнерка')
        verbose_name_plural = _ul('Партнерки')


class Advert(models.Model):
    key = models.CharField(
        verbose_name=_ul('ключ'),
        max_length=255,
        unique=True,
        help_text=_ul('Уникальное имя для обращения в шаблоне, лучше использовать латиницу без пробелов'))

    content = models.TextField(
        verbose_name=_ul('Содержимое'),
        help_text=_ul('Содержимое блока'))

    partner = models.ForeignKey(
        Partner,
        verbose_name=_ul("Партнерка"),
        help_text=_ul("Название партнерки"), on_delete=models.CASCADE)

    def __str__(self):
        return self.key

    def save(self, *args, **kwargs):
        return super(Advert, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _ul('Реклама')
        verbose_name_plural = _ul('Реклама')
