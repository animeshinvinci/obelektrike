from bs4 import BeautifulSoup as bs
from django import forms
from django.utils.translation import ugettext_lazy as _ul


def form_fields_to_bootstrap(fields):
    for key in fields:
        field = fields[key]
        if field is None:
            continue
        field.widget.attrs.update({'class': field.widget.attrs.get('class', '') + ' form-control'})
        field.widget.attrs.update({'placeholder': field.label if field.label else ''})
        if field.__class__.__name__ in (
            'DateTimeField',
            'DateField',
        ):
            field.widget.attrs.update({'class': field.widget.attrs.get('class', '') + ' datepicker'})
            field.widget.attrs.update({'style': field.widget.attrs.get('style', '') + ' width: 100%;'})
        if field.__class__.__name__ in (
            'ChoiceField',
            'ModelChoiceField',
            'MultipleChoiceField',
            'ModelMultipleChoiceField'
        ):
            field.widget.attrs.update({'style': field.widget.attrs.get('style', '') + ' width: 100%;'})
        if field.widget.__class__.__name__ in (
            'Textarea',
            'AdminTextareaWidget',
        ):
            field.widget.attrs.update({'class': field.widget.attrs.get('class', '') + ' full-ckeditor'})
        if field.label and field.required:
            field.label += ' *'


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


class BootstrapForm(SpamMixin, forms.Form):

    def __init__(self, *args, **kwargs):
        super(BootstrapForm, self).__init__(*args, **kwargs)
        form_fields_to_bootstrap(self.fields)


class BootstrapModelForm(SpamMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BootstrapModelForm, self).__init__(*args, **kwargs)
        form_fields_to_bootstrap(self.fields)
