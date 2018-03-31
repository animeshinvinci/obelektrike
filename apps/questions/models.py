from django.utils.translation import ugettext_lazy as _ul
from slugify import slugify

from apps.blogs.models import Category, Post


class Question(Post):

    def save(self, *args, **kwargs):
        self.category = Category.objects.filter(
            is_published=True,
            categorytype=Category.CATEGORY_QUESTIONS
        ).first()
        self.picture = 'uploads/posts/default.png'
        self.announcement = self.post
        self.slug = slugify(self.title)
        self.seo_title = self.title
        self.seo_description = self.title
        self.seo_keywords = self.title
        self.seo_author = self.author.get_full_name()
        return super(Question, self).save(*args, **kwargs)

    class Meta:
        proxy = True
        verbose_name = _ul('Вопрос')
        verbose_name_plural = _ul('Вопросы')
