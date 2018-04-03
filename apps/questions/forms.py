from django import forms
from django.utils.translation import ugettext_lazy as _ul

from apps.questions.models import Question
from apps.generic.forms import BootstrapModelForm


class QuestionForm(BootstrapModelForm):

    post = forms.CharField(widget=forms.Textarea, label=_ul('Вопрос')) 

    def clean_post(self):
        post = self.cleaned_data['post']
        self.clean_on_spam(post)
        return post

    class Meta:
        model = Question
        fields = ('title', 'post',)
