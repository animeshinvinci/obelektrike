from bs4 import BeautifulSoup as bs

from django import forms
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _ul


class MessageMixin(object):
    success_msg = None
    extra_tags = None

    def get_success_msg(self):
        return self.success_msg

    def form_valid(self, form):
        result = super(MessageMixin, self).form_valid(form)
        success_msg = self.get_success_msg()
        if success_msg:
            messages.success(self.request, success_msg, extra_tags=self.extra_tags)
        return result

    def form_invalid(self, form):
        result = super(MessageMixin, self).form_invalid(form)
        if form.errors:
            if '__all__' in form.errors.keys():
                messages.error(self.request, form.errors['__all__'].as_text(), extra_tags=self.extra_tags)
            else:
                messages.error(self.request, _ul(u'* Ошибки ввода'), extra_tags=self.extra_tags)
        return result


class SpamMixin(object):
    def clean_on_spam(self, text):
        msg = _ul(u'Система пометила Ваше сообщение как спам. Возможно Вы используете ссылки или Ваше сообщение содержит спам') # noqa
        is_spam = False
        soup = bs(text, "html.parser")
        hrefs = soup.findAll('a')
        if hrefs or 'http' in text or 'https' in text or 'www' in text:
            is_spam = True
        if is_spam:
            raise forms.ValidationError(msg)
