from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils.translation import ugettext_lazy as _ul

from apps.generic.models import GenericSeoModel, GenericDateModel


class SeoPage(GenericSeoModel):
    url = models.CharField(
        verbose_name=_ul('Относительный адрес'),
        unique=True,
        max_length=255,
    )

    class Meta:
        verbose_name = _ul('Страница')
        verbose_name_plural = _ul('Страницы')

    def __str__(self):
        return u'%s' % self.url


class Poll(GenericDateModel):
    question = models.CharField(
        verbose_name=_ul('Вопрос'),
        max_length=255)
    is_published = models.BooleanField(
        verbose_name=_ul('Опубликован?'),
        default=False,
        db_index=True)

    class Meta:
        verbose_name = _ul('Опрос')
        verbose_name_plural = _ul('Опросы')

    def __str__(self):
        return u'%s' % self.question


class PollItem(GenericDateModel):
    poll = models.ForeignKey(
        Poll,
        verbose_name=_ul('Опрос'),
        related_name="items",
        on_delete=models.CASCADE)
    rate = models.IntegerField(
        verbose_name=_ul('Кол-во за'),
        default=0)
    answer = models.CharField(
        verbose_name=_ul('Ответ'),
        max_length=255)

    @property
    def rate_percentage(self):
        total = sum(self.poll.items.all().values_list('rate', flat=True))
        if total:
            return int(float(self.rate * 100) / float(total))
        return 0

    def vote_action(self, session):
        if self.poll.has_session_key(session, 'pollitem_vote', setup=True):
            return
        self.rate += 1
        self.save(update_fields=('rate',))

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
