from django.core.management.base import BaseCommand

from apps.blogs.models import Post


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for post in Post.objects.all():
            post.num_comments = post.comments().count()
            post.save(update_fields=['num_comments'])
