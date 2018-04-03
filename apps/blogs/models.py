from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _ul
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from apps.generic.models import GenericDateModel, GenericSeoModel
from apps.users.models import User


class Tag(GenericDateModel):
    name = models.CharField(
        verbose_name=_ul('Имя'),
        max_length=255,
        unique=True)

    class Meta:
        ordering = ('-creation_date',)
        verbose_name = _ul('Метка')
        verbose_name_plural = _ul('Метки')

    def __str__(self):
        return u'%s' % self.name


class Category(GenericSeoModel):
    CATEGORY_NONE = 0
    CATEGORY_QUESTIONS = 1
    CATEGORY_NEWS = 2
    CATEGORY_PRACTICS = 3
    CATEGORY_TYPES = (
        (CATEGORY_NONE, _ul('Обычная категория')),
        (CATEGORY_QUESTIONS, _ul('Категория вопроса')),
        (CATEGORY_NEWS, _ul('Категория новости')),
        (CATEGORY_PRACTICS, _ul('Категория практики')),
    )

    name = models.CharField(
        verbose_name=_ul('Имя'),
        max_length=255,
        unique=True)
    categorytype = models.PositiveSmallIntegerField(
        verbose_name=_ul('Тип категории'),
        choices=CATEGORY_TYPES,
        default=CATEGORY_NONE,
        db_index=True)
    description = models.TextField(
        verbose_name=_ul('Описание'),
        null=True,
        blank=True)
    image_class = models.CharField(
        verbose_name=_ul('Класс картинки'),
        max_length=255,
        null=True,
        blank=True)

    def get_absolute_url(self):
        if self.is_published:
            return u'/category/%s/' % self.slug

    class Meta:
        ordering = ('-creation_date',)
        verbose_name = _ul('Категория')
        verbose_name_plural = _ul('Категории')

    def __str__(self):
        return u'%s' % self.name


class Post(GenericSeoModel):
    category = models.ForeignKey(
        Category,
        verbose_name=_ul('Категория'),
        on_delete=models.CASCADE)
    tags = models.ManyToManyField(
        Tag,
        verbose_name=_ul('Метки'),
        blank=True)
    author = models.ForeignKey(
        User,
        verbose_name=_ul('Автор статьи'),
        related_name='author_posts',
        on_delete=models.CASCADE)
    picture = models.ImageField(
        verbose_name=_ul('Главная картинка'),
        upload_to=u'uploads/posts/',
        null=True,
        blank=True)

    title = models.CharField(
        verbose_name=_ul('Заголовок'),
        max_length=255,
        unique=True)
    announcement = RichTextUploadingField(
        verbose_name=_ul('Анонс'))
    post = RichTextUploadingField(
        verbose_name=_ul('Статья'))

    view_count = models.IntegerField(
        verbose_name=_ul('Кол-во просмотров'),
        default=0)
    rate = models.IntegerField(
        verbose_name=_ul('Кол-во лайков'),
        default=0)
    num_comments = models.IntegerField(
        verbose_name=_ul('Кол-во комментариев'),
        default=0)

    publication_date = models.DateTimeField(
        verbose_name=_ul('Дата публикации'),
        null=True,
        blank=True)

    notes = RichTextUploadingField(
        verbose_name=_ul('Notes'),
        null=True,
        blank=True)

    def comments(self):
        return Comment.objects.filter(post=self, is_published=True)

    def get_absolute_url(self):
        if self.is_published:
            return u'/posts/%s/' % self.slug

    def view_action(self, session):
        if self.has_session_key(session, 'post_view', setup=True):
            return
        self.view_count += 1
        self.save(update_fields=['view_count'])

    def like_action(self, session):
        if self.has_session_key(session, 'post_like', setup=True):
            return
        self.rate += 1
        self.save(update_fields=['rate'])

    def unlike_action(self, session):
        if self.has_session_key(session, 'post_like', setup=True):
            return
        self.rate -= 1
        self.save(update_fields=['rate'])

    def post_mini_shorter(self):
        return str(self.announcement)[:100] + "..."

    def is_question(self):
        return self.category.categorytype == Category.CATEGORY_QUESTIONS

    def save(self, *args, **kwargs):
        if self.publication_date is None and self.is_published:
            self.publication_date = timezone.now()
        # User.objects.send_email_to_subscribers(self)
        return super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-publication_date',)
        verbose_name = _ul('Статья')
        verbose_name_plural = _ul('Статьи')

    def __str__(self):
        return u'%s' % self.title


class Comment(MPTTModel, GenericDateModel):
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name="comment_parent",
        verbose_name=_ul('Родительский комментарий'),
        on_delete=models.CASCADE)

    post = models.ForeignKey(
        Post,
        verbose_name=_ul('Статья'),
        on_delete=models.CASCADE)
    author = models.ForeignKey(
        User,
        verbose_name=_ul('Автор'),
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    author_username = models.CharField(
        verbose_name=_ul('Имя автора'),
        max_length=255)
    comment = RichTextUploadingField(
        verbose_name=_ul('Комментарий'),
        config_name='comment')
    is_spam = models.BooleanField(
        verbose_name=_ul('Спам?'),
        default=False)
    is_published = models.BooleanField(
        verbose_name=_ul('Опубликован?'),
        default=True,
        db_index=True)

    rate = models.IntegerField(
        verbose_name=_ul('Кол-во лайков'),
        default=0)

    ip_address = models.CharField(
        verbose_name = _ul('IP address'),
        max_length=255,
        null=True,
        blank=True)

    def get_absolute_url(self):
        if self.is_published and self.post.is_published:
            return self.post.get_absolute_url() + '#comment_%s' % self.pk

    def like_action(self, session):
        if self.has_session_key(session, 'comment_like', setup=True):
            return
        self.rate += 1
        self.save(update_fields=['rate'])

    def unlike_action(self, session):
        if self.has_session_key(session, 'comment_like', setup=True):
            return
        self.rate -= 1
        self.save(update_fields=['rate'])

    def save(self, *args, **kwargs):
        if self.author:
            self.author_username = self.author.get_full_name()
        return super(Comment, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-creation_date',)
        verbose_name = _ul('Комментарий')
        verbose_name_plural = _ul('Комментарии')

    def __str__(self):
        return u'%s' % self.comment
