"""
WSGI config for obelektrike project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
import environ

from django.core.wsgi import get_wsgi_application

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

environ.Env.read_env(os.path.join(BASE_DIR, 'env.prod'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "obelektrike.settings")

application = get_wsgi_application()
