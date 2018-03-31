from django.core.management.commands import makemessages

additional_opts = [
    '--keyword=_i',
    '--keyword=_u',
    '--keyword=_ul',
]


class Command(makemessages.Command):
    xgettext_options = makemessages.Command.xgettext_options + additional_opts
