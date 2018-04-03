import uuid

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _ul
from django.views.generic import DetailView, FormView, RedirectView, UpdateView

from apps.cms.utils import send_mail
from apps.generic.mixins import MessageMixin
from apps.users.forms import (
    LoginForm, PasswordChangeForm, PasswordResetForm, RegistrationForm,
    SubscribeForm, UserForm,
)
from apps.users.models import User


class LoginView(MessageMixin, FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def get_success_url(self):
        next_url = self.request.GET.get('next', None)
        if next_url is not None:
            return next_url
        return reverse_lazy('index')

    def form_valid(self, form):
        user = form.cleaned_data['user']
        if user is not None:
            login(self.request, user)
            cache.clear()
        return super(LoginView, self).form_valid(form)


class LogoutView(RedirectView):
    url = reverse_lazy('index')

    def get_redirect_url(self):
        logout(self.request)
        cache.clear()
        next_url = self.request.GET.get('next', None)
        if next_url is not None:
            return next_url
        return super(LogoutView, self).get_redirect_url()

    @method_decorator(login_required(login_url=reverse_lazy('u-login')))
    def dispatch(self, *args, **kwargs):
        return super(LogoutView, self).dispatch(*args, **kwargs)


class RegistrationView(MessageMixin, FormView):
    template_name = 'registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('u-login')
    success_msg = _ul(
        'Ссылка для окончания регистрации отправлена Вам на почту'
        '(если письмо не пришло поищите его в спаме).'
    )

    def send_registration(self, user, key):
        registration_url = 'http://obelektrike.ru' + reverse('u-registration-uuid', kwargs={'uuid': key})
        message = _ul("""
            Для окончания регистрации перейдите по следующей ссылке:\n
            %s \n
            \n
            С уважением,
            Команда obelektrike.ru
            """) % registration_url
        send_mail(
            subject=_ul(u'Регистрация пользователя на сайте obelektrike.ru'),
            message=message,
            from_email=settings.SUPPORT_EMAIL,
            recipient_list=[user.email],
            fail_silently=True
        )

    def form_valid(self, form):
        key = uuid.uuid4()
        user = User.objects.create(
            username=form.cleaned_data['email'],
            registration_key=key,
            is_active=False,
        )
        user.set_password(form.cleaned_data['password'])
        user.save()
        self.send_registration(user, key)
        return super(RegistrationView, self).form_valid(form)


class RegistrationUuidView(RedirectView):
    url = reverse_lazy('index')

    def get_redirect_url(self, *args, **kwargs):
        try:
            self.user = User.objects.get(registration_key=kwargs['uuid'])
        except User.DoesNotExist:
            raise Http404
        self.user.is_active = True
        self.user.registration_key = None
        self.user.save()
        return super(RegistrationUuidView, self).get_redirect_url()


class PasswordResetView(MessageMixin, FormView):
    template_name = 'password-reset.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('u-reset-password')
    success_msg = _ul(u'Ссылка для сброса пароля отправлена Вам на почту (если письмо не пришло поищите его в спаме).')

    def send_resetpassword(self, user, key):
        reset_url = 'http://obelektrike.ru' + reverse('u-reset-password-uuid', kwargs={'uuid': key})
        message = _ul("""
            Для сброса пароль перейдите по следующей ссылке:\n
            %s \n
            \n
            С уважением,
            Команда obelektrike.ru
            """) % reset_url
        send_mail(
            subject=_ul(u'Сброс пароля для пользователя %s на obelektrike.ru') % user.get_full_name(),
            message=message,
            from_email=settings.SUPPORT_EMAIL,
            recipient_list=[user.email],
            fail_silently=True
        )

    def form_valid(self, form):
        key = uuid.uuid4()
        user = User.objects.get(username=form.cleaned_data['email'])
        user.reset_password_key = key
        user.save()
        self.send_resetpassword(user, key)
        return super(PasswordResetView, self).form_valid(form)


class PasswordResetUuidView(MessageMixin, FormView):
    template_name = 'password.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('u-login')
    success_msg = _ul(u'Пароль успешно изменен. Зайдите используя новый пароль.')

    def form_valid(self, form):
        self.user.set_password(form.cleaned_data['password'])
        self.user.reset_password_key = None
        self.user.save()
        return super(PasswordResetUuidView, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        try:
            self.user = User.objects.get(reset_password_key=self.kwargs['uuid'])
        except User.DoesNotExist:
            raise Http404
        return super(PasswordResetUuidView, self).dispatch(*args, **kwargs)


class PasswordChangeView(MessageMixin, FormView):
    template_name = 'password.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        self.request.user.set_password(form.cleaned_data['password'])
        self.request.user.save()
        return super(PasswordChangeView, self).form_valid(form)

    @method_decorator(login_required(login_url=reverse_lazy('u-login')))
    def dispatch(self, *args, **kwargs):
        return super(PasswordChangeView, self).dispatch(*args, **kwargs)


class UserUpdateView(MessageMixin, UpdateView):
    template_name = 'user-update.html'
    form_class = UserForm
    model = User

    def get_object(self, queryset=None):
        obj = super(UserUpdateView, self).get_object(queryset=queryset)
        if self.request.user.is_staff or self.request.user.pk == obj.pk:
            return obj
        raise Http404

    def get_success_url(self):
        return reverse_lazy('u-profile', kwargs={'pk': self.object.pk})

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserUpdateView, self).dispatch(*args, **kwargs)


class UserDetailView(DetailView):
    template_name = 'user.html'
    model = User


class SubscribeUser(MessageMixin, FormView):
    template_name = ''
    form_class = SubscribeForm
    extra_tags = 'subscribe'
    success_msg = _ul(u'Теперь уведомление о каждой новой статьи будет приходить Вам на email.')

    def get(self, request, *args, **kwargs):
        raise Http404

    def get_success_url(self):
        next_url = self.request.GET.get('next', None)
        if next_url is not None:
            return next_url
        return reverse_lazy('index')

    def form_valid(self, form):
        user, _ = User.objects.get_or_create(
            username=form.cleaned_data['email'],
            defaults=dict(
                email=form.cleaned_data['email'],
                is_active=False
            )
        )
        user.is_subscribe = True
        user.date_subscribe = timezone.now()
        user.save()
        return super(SubscribeUser, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors.as_text(), extra_tags=self.extra_tags)
        return redirect(self.get_success_url())
