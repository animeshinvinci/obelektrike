from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _ul
from django.views.generic import CreateView, ListView

from apps.generic.mixins import MessageMixin
from apps.blogs.models import Category
from apps.questions.forms import QuestionForm
from apps.questions.models import Question


class QuestionListView(ListView):
    model = Question
    paginate_by = 10
    template_name = 'question-list.html'

    def get_queryset(self):
        qs = super(QuestionListView, self).get_queryset()
        return qs.filter(is_published=True).filter(category__categorytype=Category.CATEGORY_QUESTIONS)


class QuestionUserListView(QuestionListView):
    template_name = 'question-user-list.html'

    def get_queryset(self):
        qs = super(QuestionUserListView, self).get_queryset()
        return qs.filter(author=self.request.user)

    @method_decorator(login_required(login_url=reverse_lazy('u-login')))
    def dispatch(self, *args, **kwargs):
        return super(QuestionUserListView, self).dispatch(*args, **kwargs)


class QuestionCreateView(MessageMixin, CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'question-create.html'
    success_url = reverse_lazy('u-questions-list')
    success_msg = _ul('Ваш вопрос опубликован.')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(QuestionCreateView, self).form_valid(form)

    @method_decorator(login_required(login_url=reverse_lazy('u-login')))
    def dispatch(self, *args, **kwargs):
        return super(QuestionCreateView, self).dispatch(*args, **kwargs)
