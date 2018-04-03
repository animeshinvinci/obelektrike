from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        call_command('migrate', interactive=False)
        call_command('collectstatic', interactive=False)
        # call_command('compilemessages')
        call_command('synccomments')
        call_command('cleancache')
        if not settings.DEBUG:
            call_command('compress')
