from django.conf import settings
from django.http import Http404, JsonResponse
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _ul
from django.views.generic import CreateView, TemplateView

from apps.cms.forms import FeedbackForm
from apps.cms.models import Feedback, PollItem
from apps.email.utils import send_mail
from apps.generic.mixins import MessageMixin


class FlatPageDetailView(TemplateView):
    template_name = 'page.html'


class FeedbackCreateView(MessageMixin, CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'feedback.html'
    success_url = reverse_lazy('feedback')
    success_msg = _ul(u'Ваше сообщение отправлено нам на почту. Мы свяжемся с вами в ближайшее время.')

    def send_feedback(self, feedback):
        admins = [admin[1] for admin in settings.ADMINS]
        send_mail(
            subject=_ul(u'Вам написал пользователь %s %s на obelektrike.ru') % (feedback.name, feedback.email),
            message=feedback.message,
            from_email=settings.SUPPORT_EMAIL,
            recipient_list=admins + [settings.SUPPORT_EMAIL],
            fail_silently=True,
            html_message=feedback.message
        )

    def form_valid(self, form):
        result = super(FeedbackCreateView, self).form_valid(form)
        self.send_feedback(form.instance)
        return result


def cms_vote(request):
    pk = request.POST.get('pk', None)
    if pk is not None and pk.isdigit():
        obj = PollItem.objects.filter(pk=pk).first()
        if obj is not None:
            obj.vote_action(request.session)
            return JsonResponse({})
    raise Http404
