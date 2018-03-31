from django.db import models
from django.utils.translation import ugettext_lazy as _ul

from apps.generic.models import GenericDateModel


class Email(GenericDateModel):
    from_email = models.CharField(blank=True, default='', max_length=255)
    to_emails = models.TextField(blank=True, default='')

    subject = models.TextField(blank=True, default='')
    body = models.TextField(blank=True, default='')

    def __str__(self):
        return u'Email from "%s" to "%s" sent at %s about "%s"' % (
            self.from_email,
            self.to_emails,
            self.creation_date,
            self.subject
        )

    class Meta:
        verbose_name = _ul('Email')
        verbose_name_plural = _ul('Emails')
        ordering = ['-creation_date']
