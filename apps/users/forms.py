from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _ul

from apps.generic.forms import BootstrapForm, BootstrapModelForm
from apps.users.models import User


class LoginForm(BootstrapForm):
    email = forms.EmailField(
        max_length=255,
        label=_ul('Введите вашу почту')
    )
    password = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(),
        label=_ul('Введите ваш пароль')
    )

    def clean(self):
        self.cleaned_data = super(LoginForm, self).clean()
        if (
            'password' in self.cleaned_data and
            'email' in self.cleaned_data
        ):
            self.cleaned_data['user'] = authenticate(
                username=self.cleaned_data['email'],
                password=self.cleaned_data['password']
            )
            if not self.cleaned_data['user']:
                raise forms.ValidationError(
                    _ul('Не правильно введена почта или пароль.')
                )
        return self.cleaned_data


class PasswordResetForm(BootstrapForm):
    email = forms.EmailField(label=_ul('Введите вашу почту'))

    def clean_email(self):
        qs = User.objects.filter(username=self.cleaned_data['email'])
        if not qs.exists():
            raise forms.ValidationError(_ul('Пользователь с такой почтой не существует.'))
        return self.cleaned_data['email']


class PasswordChangeForm(BootstrapForm):
    password = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(),
        label=_ul('Ваш новый пароль')
    )
    confirm_password = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(),
        label=_ul('Повторите ваш новый пароль')
    )

    def clean_confirm_password(self):
        if not self.cleaned_data['password'] == self.cleaned_data['confirm_password']:
            raise forms.ValidationError(_ul('Пароли не совпадают.'))
        return self.cleaned_data['confirm_password']


class RegistrationForm(BootstrapForm):
    email = forms.EmailField(label=_ul('Введите вашу почту'))
    password = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(),
        label=_ul('Ваш новый пароль')
    )
    confirm_password = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(),
        label=_ul('Повторите ваш новый пароль')
    )

    def clean_email(self):
        qs = User.objects.filter(username=self.cleaned_data['email'])
        if qs.exists():
            raise forms.ValidationError(_ul('Пользователь с такой почтой уже существует.'))
        return self.cleaned_data['email']

    def clean_confirm_password(self):
        if not self.cleaned_data['password'] == self.cleaned_data['confirm_password']:
            raise forms.ValidationError(_ul('Пароли не совпадают.'))
        return self.cleaned_data['confirm_password']


class SubscribeForm(BootstrapForm):
    email = forms.EmailField(label=_ul('Введите вашу почту'))

    def clean_email(self):
        qs = User.objects.filter(username=self.cleaned_data['email'], is_subscribe=True)
        if qs.exists():
            raise forms.ValidationError(_ul('Пользователь с такой почтой уже подписан.'))
        return self.cleaned_data['email']


class UserForm(BootstrapModelForm):
    username = forms.EmailField(label=_ul('Логин'))
    nickname = forms.CharField(label=_ul('Ник'))

    class Meta:
        model = User
        fields = ('username', 'nickname', 'first_name', 'last_name', 'avatar', 'city', 'about',)
