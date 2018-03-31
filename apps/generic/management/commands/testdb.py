from random import randint

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from apps.blogs.models import Category, Comment, Post
from apps.cms.models import Material
from apps.users.models import User


class Command(BaseCommand):

    def create_cms_pages(self):
        for material_type in getattr(settings, 'MATERIAL_TYPES', ()):
            Material.objects.get_or_create(
                pagetype=material_type[0],
                defaults=dict(
                    title=material_type[1],
                    data='',
                )
            )

    def create_users(self):
        admin, _ = User.objects.get_or_create(username='admin@admin.com')
        admin.is_superuser = True
        admin.is_staff = True
        admin.is_active = True
        admin.set_password('1111')
        admin.save()
        for i in range(1, 5):
            u, _ = User.objects.get_or_create(username='user_%s@user.com' % i)
            u.is_active = True
            u.set_password('1111')
            u.save()
        self.stdout.write("Create initial users")

    def create_categories(self):
        for i in range(1, 5):
            category, _ = Category.objects.get_or_create(
                name='category %s' % i, slug=slugify('category %s' % i)
            )
            category.is_published = True
            category.save()
        self.stdout.write("Create test categories")

    def create_tags(self):
        self.stdout.write("Create test tags")

    def create_posts(self):
        self.create_categories()
        self.create_tags()
        for i in range(50):
            ruser = User.objects.order_by('?')[:1][0]
            rcategory = Category.objects.order_by('?')[:1][0]
            rrate = randint(-10, 10)
            ris_published = bool(randint(0, 1))
            pictures_url = 'uploads/posts/default.png'
            defaults = dict(
                category=rcategory,
                author=ruser
            )
            post, _ = Post.objects.get_or_create(
                title='Lorem %s %s' % (ruser, i),
                picture=pictures_url,
                defaults=defaults
            )
            post.slug = slugify(post.title)
            post.category = rcategory
            post.post = 'Lorem %s %s' % (ruser, i)
            post.rate = rrate
            post.is_published = ris_published
            post.author = ruser
            post.save()
        self.stdout.write("Create test posts")

    def create_comments(self):
        for post in Post.objects.all():
            for i in range(10):
                ruser = User.objects.order_by('?')[:1][0]
                comment = Comment(post=post, author=ruser, comment='Lorem %s %s' % (ruser, i), is_published=True)
                comment.save()
        self.stdout.write("Create test comments")

    def handle(self, *args, **kwargs):
        call_command('initenv')
        self.create_cms_pages()
        self.create_users()
        self.create_posts()
        self.create_comments()
