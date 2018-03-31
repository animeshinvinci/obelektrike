from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _ul

from apps.email.utils import send_mail


class ExtUserManager(UserManager):

    def send_email_to_subscribers(self, post):
        post_url = 'http://obelektrike.ru' + reverse('posts-category-detail', kwargs={'slug': post.slug})
        message = _ul("""
            С удовольствием сообщаем, что на портале obelektrike.ru появилась новая статья:\n
            %s \n
            %s \n
            \n
            С уважением,
            Команда obelektrike.ru
            """) % (post.title, post_url)
        emails = list(self.filter(is_subscribe=True).values_list('email', flat=True))
        for email in emails:
            send_mail(
                subject=_ul('Новые статья на сайте obelektrike.ru'),
                message=message,
                from_email=settings.SUPPORT_EMAIL,
                recipient_list=[email],
                fail_silently=True
            )


class User(AbstractUser):
    username = models.CharField(
        _ul('username'),
        max_length=255,
        unique=True,
        help_text=_ul('Required. 255 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[AbstractUser.username_validator],
        error_messages={
            'unique': _ul("A user with that username already exists."),
        },
    )

    nickname = models.CharField(verbose_name=_ul('Ник'), max_length=255, null=True, blank=True)
    avatar = models.FileField(verbose_name=_ul('Аватар'), upload_to='users/', default='defaults/user.jpeg')
    about = RichTextUploadingField(verbose_name=_ul('О себе'), null=True, blank=True)
    city = models.CharField(verbose_name=_ul('Город'), max_length=128, default='', blank=True)

    reset_password_key = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_ul('Ключ сброс пароля'),
        unique=True
    )
    registration_key = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_ul('Ключ регистрация'),
        unique=True
    )

    is_subscribe = models.BooleanField(verbose_name=_ul('Подписан'), default=False)
    date_subscribe = models.DateTimeField(verbose_name=_ul('Дата подписки'), null=True, blank=True)

    objects = ExtUserManager()

    def get_full_name(self):
        if self.nickname is not None and self.nickname:
            return self.nickname
        if self.first_name and self.last_name:
            return "%s %s" % (self.first_name, self.last_name)
        return self.username

    def save(self, *args, **kwargs):
        self.email = self.username
        if self.nickname is None:
            self.nickname = self.username.split('@')[0]
        return super(User, self).save(*args, **kwargs)
